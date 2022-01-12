
@Subroutine(TealType.none)
def pay(amount: TealType.uint64, receiver: TealType.bytes):
    InnerTxnBuilder.Begin()
    InnerTxnBuilder.SetFields({
        TxnField.type_enum: TxnType.Payment,
        TxnField.sender: Global.current_application_address(),
        TxnField.amount: amount,
        TxnField.receiver: receiver
        })
    InnerTxnBuilder.Submit()

def teal():
    pay(Int(10), Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY'))
    result = Int(0)
    if Txn.first_valid() > Int(1000000):
        result = Int(1)

    return result

