
def pay(amount: uint64, receiver: bytes):
    Begin()
    SetFields({
        TxnField.type_enum: TxnType.Payment,
        TxnField.sender: Global.current_application_address(),
        TxnField.amount: amount,
        TxnField.receiver: receiver
        })
    Submit()

def teal():
    pay(10, Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY'))
    result = 0
    if Txn.first_valid() > 1000000:
        result = 1
    return result

