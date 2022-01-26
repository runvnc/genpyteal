import json
from pyteal import *
from pytealutils.applications import ABIMethod
from pytealutils.applications import DefaultApprove
from pytealutils import abi


class KitchenSink(DefaultApprove):
    @staticmethod
    @ABIMethod
    def reverse(a: abi.String) -> abi.String:
        @Subroutine(TealType.bytes)
        def reverse(a: TealType.bytes) -> Expr:
            return (
                If(Len(a) == Int(0))
                .Then(Bytes(""))
                .Else(
                    Concat(
                        Extract(a, Len(a) - Int(1), Int(1)),
                        reverse(Extract(a, Int(0), Len(a) - Int(1))),
                    )
                )
            )

        return reverse(a)

    @staticmethod
    @ABIMethod
    def split(a: abi.String) -> abi.DynamicArray[abi.String]:
        l = abi.DynamicArray[abi.String](Bytes(""))

        @Subroutine(TealType.none)
        def rsplit(
            data: TealType.bytes, idx: TealType.uint64, lastIdx: TealType.uint64
        ) -> Expr:
            return If(
                Len(data) == idx,  # we're finished, append the last one
                l.append(Substring(data, lastIdx, idx)),
                If(
                    GetByte(data, idx) == Int(32),
                    Seq(
                        l.append(Substring(data, lastIdx, idx)),
                        rsplit(data, idx + Int(1), idx),
                    ),
                    rsplit(data, idx + Int(1), lastIdx),
                ),
            )

        return Seq(l.init(), rsplit(a, Int(0), Int(0)), l.serialize())

    @staticmethod
    @ABIMethod
    def concat(a: abi.DynamicArray[abi.String]) -> abi.String:
        idx = ScratchVar()
        buff = ScratchVar()
        return Seq(
            buff.store(Bytes("")),
            For(
                idx.store(Int(0)),
                idx.load() < a.size.load(),
                idx.store(idx.load() + Int(1)),
            ).Do(buff.store(Concat(buff.load(), Bytes(" "), a[idx.load()]))),
            buff.load(),
        )

    @staticmethod
    @ABIMethod
    def add(a: abi.Uint32, b: abi.Uint32) -> abi.Uint32:
        return a + b

    @staticmethod
    @ABIMethod
    def sub(a: abi.Uint32, b: abi.Uint32) -> abi.Uint32:
        return a - b

    @staticmethod
    @ABIMethod
    def div(a: abi.Uint32, b: abi.Uint32) -> abi.Uint32:
        return a / b

    @staticmethod
    @ABIMethod
    def mul(a: abi.Uint32, b: abi.Uint32) -> abi.Uint32:
        return a * b


if __name__ == "__main__":
    app = KitchenSink()

    with open("interface.json", "w") as f:
        f.write(json.dumps(app.get_interface().dictify()))

    with open("approval.teal", "w") as f:
        f.write(
            compileTeal(
                app.handler(), mode=Mode.Application, version=5, assembleConstants=True
            )
        )
