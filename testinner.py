
def inner_payment_txn(amount: TealType.uint64, receiver: TealType.bytes):
  InnerTxnBuilder.Begin()
  InnerTxnBuilder.SetFields({
      TxnField.type_enum: TxnType.Payment,
      TxnField.sender: Global.current_application_address(),
      TxnField.amount: amount,
      TxnField.receiver: receiver
      })
  InnerTxnBuilder.Submit()

