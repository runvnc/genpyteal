from abc import ABC, abstractmethod
from typing import List
from inspect import signature, _empty
from functools import wraps
from Cryptodome.Hash import SHA512
import base64
import sys

from algosdk import abi
from algosdk.account import address_from_private_key
from algosdk.v2client import algod
from algosdk.future.transaction import (
    ApplicationDeleteTxn,
    ApplicationUpdateTxn,
    ApplicationCreateTxn,
    StateSchema,
    wait_for_confirmation,
    OnComplete as oc,
)
from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
    AtomicTransactionComposer,
    TransactionWithSigner,
)

from pyteal import *

from .. import abi as tealabi


# Utility function to take the string version of a
# method signature and return the 4 byte selector
def hashy(method: str) -> Bytes:
    chksum = SHA512.new(truncate="256")
    chksum.update(method.encode())
    return Bytes(chksum.digest()[:4])


@Subroutine(TealType.none)
def ABIReturn(b: TealType.bytes) -> Expr:
    return Log(Concat(Bytes("base16", "0x151f7c75"), b))


def ABIMethod(func):
    sig = signature(func)

    args1 = []
    for v in sig.parameters.values():
      if v.annotation != _empty:
        args1.append(( v.annotation.__str__(), v.name ))
      else:
        args1.append(( v.name, '' ))

    #args = [tealabi.abiTypeName(v.annotation) for v in sig.parameters.values()]

    args = []
    for v in sig.parameters.values():
      if v.name in ['asset', 'account', 'application']:
        args.append(v.name)
      else:
        args.append(tealabi.abiTypeName(v.annotation))
    
    returns = sig.return_annotation

    method = "{}({}){}".format(
        func.__name__, ",".join(args), tealabi.abiTypeName(returns)
    )

    setattr(func, "abi_selector", hashy(method))
    setattr(func, "abi_args", [abi.Argument(type, name) for (type, name) in args1])
    setattr(func, "abi_returns", abi.Returns(tealabi.abiTypeName(returns)))

    # Get the types specified in the method
    #abi_codec = [v.annotation for v in sig.parameters.values()]

    abi_codec = []
    for v in sig.parameters.values():
      if v.name in ['asset', 'account', 'application']:
        abi_codec.append(Uint8)
      else:
        abi_codec.append(v.annotation)
    
    @wraps(func)
    @Subroutine(TealType.uint64)
    def wrapper() -> Expr:
        decoded = [
            abi_codec[idx](Txn.application_args[idx + 1])
            for idx in range(len(abi_codec))
        ]

        return Seq(
            # Initialize scratch space for complex types
            *[d.init() for d in decoded if hasattr(d, "init")],
            ABIReturn(returns.encode(func(*decoded))),
            Int(1),
        )

    return wrapper


class Application(ABC):
    def global_schema(self) -> StateSchema:
        return StateSchema(0, 0)

    def local_schema(self) -> StateSchema:
        return StateSchema(0, 0)

    @abstractmethod
    def create(self) -> Expr:
        pass

    @abstractmethod
    def update(self) -> Expr:
        pass

    @abstractmethod
    def delete(self) -> Expr:
        pass

    @abstractmethod
    def optIn(self) -> Expr:
        pass

    @abstractmethod
    def closeOut(self) -> Expr:
        pass

    @abstractmethod
    def clearState(self) -> Expr:
        pass

    @classmethod
    def get_methods(cls) -> List[str]:
        return list(set(dir(cls)) - set(dir(cls.__base__)))

    def handler(self) -> Expr:
        methods = self.get_methods()
       
        withABI = filter(lambda m: hasattr(getattr(self,m), 'abi_args'), self.get_methods())
        
        routes = [
            [Txn.application_args[0] == f.abi_selector, f()]
            for f in map(lambda m: getattr(self, m), withABI)
        ]

        # Hack to add budget padding
        routes.append([Txn.application_args[0] == hashy("pad()void"), Int(1)])

        handlers = [
            [Txn.application_id() == Int(0), self.create()],
            [
                Txn.on_completion() == OnComplete.UpdateApplication,
                self.update(),
            ],
            [
                Txn.on_completion() == OnComplete.DeleteApplication,
                self.delete(),
            ],
            *routes,
            [Txn.on_completion() == OnComplete.OptIn, self.optIn()],
            [Txn.on_completion() == OnComplete.CloseOut, self.closeOut()],
            [Txn.on_completion() == OnComplete.ClearState, self.clearState()],
        ]

        return Cond(*handlers)

    def get_interface(self) -> abi.Interface:
        withABI = filter(lambda m: hasattr(getattr(self,m), 'abi_args'), self.get_methods())
        abiMethods = [
            abi.Method(f.__name__, f.abi_args, f.abi_returns)
            for f in map(lambda m: getattr(self, m), withABI)
        ]

        # TODO: hacked this in for now, to provide extended extended budget
        #abiMethods.append(abi.Method("pad", [], abi.Returns("void")))

        return abi.Interface(self.__class__.__name__, abiMethods)

    def get_contract(self, app_id: int) -> abi.Contract:
        interface = self.get_interface()
        return abi.Contract(interface.name, app_id, interface.methods)

    def create_app(
        self, client: algod.AlgodClient, signer: AccountTransactionSigner
    ) -> abi.Contract:
        sp = client.suggested_params()

        approval_result = client.compile(self.approval_source())
        approval_program = base64.b64decode(approval_result["result"])

        clear_result = client.compile(self.clear_source())
        clear_program = base64.b64decode(clear_result["result"])

        ctx = AtomicTransactionComposer()
        ctx.add_transaction(
            TransactionWithSigner(
                ApplicationCreateTxn(
                    address_from_private_key(signer.private_key),
                    sp,
                    oc.NoOpOC,
                    approval_program,
                    clear_program,
                    self.global_schema(),
                    self.local_schema(),
                ),
                signer,
            )
        )
        result = wait_for_confirmation(client, ctx.submit(client)[0])
        return self.get_contract(result["application-index"])

    def update_app(
        self, client: algod.AlgodClient, app_id: int, signer: AccountTransactionSigner
    ):
        sp = client.suggested_params()

        approval_result = client.compile(self.approval_source())
        approval_program = base64.b64decode(approval_result["result"])

        clear_result = client.compile(self.clear_source())
        clear_program = base64.b64decode(clear_result["result"])

        ctx = AtomicTransactionComposer()
        ctx.add_transaction(
            TransactionWithSigner(
                ApplicationUpdateTxn(
                    address_from_private_key(signer.private_key),
                    sp,
                    app_id,
                    approval_program,
                    clear_program,
                ),
                signer,
            )
        )
        ctx.execute(client, 2)
        return self.get_contract(app_id)

    def delete_app(
        self, client: algod.AlgodClient, app_id: int, signer: AccountTransactionSigner
    ):
        sp = client.suggested_params()

        ctx = AtomicTransactionComposer()
        ctx.add_transaction(
            TransactionWithSigner(
                ApplicationDeleteTxn(
                    address_from_private_key(signer.private_key),
                    sp,
                    app_id,
                ),
                signer,
            )
        )
        return ctx.execute(client, 2)

    def approval_source(self) -> str:
        return compileTeal(
            self.handler(), mode=Mode.Application, version=5, assembleConstants=True
        )

    def clear_source(self) -> str:
        return "#pragma version 5;int 1;return".replace(";", "\n")
