from pyteal import *

globals().update(TealType.__members__)

@Subroutine(TealType.none)
def pay(amount: uint64, receiver: bytes):
    return Seq([
    InnerTxnBuilder.Begin(),
    InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.sender: Global.current_application_address(),
            TxnField.amount: amount,
            TxnField.receiver: receiver
            })({
            TxnField.type_enum: TxnType.Payment,
            TxnField.sender: Global.current_application_address(),
            TxnField.amount: amount,
            TxnField.receiver: receiver
            }),
    InnerTxnBuilder.Submit()])


def teal():
    result = ScratchVar(TealType.uint64)
    return Seq([
    pay(Int(10), Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY')),
    result.store(Int(0)),
    If(Txn.first_valid() > Int(1000000), 
                result.store(Int(1))
            ),
    Return(result)])

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
