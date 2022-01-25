from typing import List
from algosdk.abi import Method, Contract
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    TransactionSigner,
)
from algosdk.account import address_from_private_key
from nacl.utils import random
from os import urandom

# TODO: Cache suggested params


class ContractClient:
    def __init__(
        self, client: AlgodClient, contract: Contract, signer: TransactionSigner = None
    ):
        self.client = client

        self.contract = contract
        self.app_id = contract.app_id
        self.signer = signer

        self.addr = address_from_private_key(self.signer.private_key)

        for m in self.contract.methods:
            setattr(self, m.name, m)

    def compose(self, method: Method, args: List[any], ctx: AtomicTransactionComposer):
        sp = self.client.suggested_params()
        ctx.add_method_call(
            self.app_id, method, self.addr, sp, self.signer, method_args=args
        )

    def call(self, method: Method, args: List[any], budget=1):
        ctx = AtomicTransactionComposer()

        sp = self.client.suggested_params()
        ctx.add_method_call(
            self.app_id, method, self.addr, sp, self.signer, method_args=args
        )

        for _ in range(budget - 1):
            ctx.add_method_call(
                self.app_id, self.pad, self.addr, sp, self.signer, note=urandom(5)
            )

        return ctx.execute(self.client, 2)
