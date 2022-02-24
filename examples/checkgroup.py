PAYTO = Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY')
FEE = 10 * 1000000
ZERO = Global.zero_address()

def no_close_to(i):
  Assert( Gtxn[i].close_remainder_to == ZERO )

def no_rekey(i):
  Assert( Gtxn[i].rekey_to == ZERO )

def verify_payment(i):
  Assert( Gtxn[i].receiver == PAYTO and
          Gtxn[i].amount == FEE and
          Gtxn[i].type_enum == TxnType.Payment )
         
def app():
  Assert( Global.group_size == 2 )
  
  no_close_to(1)
  no_rekey(1)

  verify_payment(1)

  gput('lastPaymentFrom', Gtxn[1].sender)
  Approve()
