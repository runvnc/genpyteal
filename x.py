from pyteal import *

globals().update(TealType.__members__)

PAYTO = Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY')
FEE = Int(10) * Int(1000000)
ZERO = Global.zero_address()

@Subroutine(TealType.none)
def no_close_to(i):
  return Assert( Gtxn[i].close_remainder_to() == ZERO )

@Subroutine(TealType.none)
def no_rekey(i):
  return Assert( Gtxn[i].rekey_to() == ZERO )

@Subroutine(TealType.none)
def verify_payment(i):
  return Assert( And( Gtxn[i].receiver() == PAYTO, And( Gtxn[i].amount() == FEE, Gtxn[i].type_enum() == TxnType.Payment ) ) )

def app():
    return  Seq(
    	Assert( Global.group_size() == Int(2) ),
    	no_close_to(Int(1)),
    	no_rekey(Int(1)),
    	verify_payment(Int(1)),
    	App.globalPut(Bytes('lastPaymentFrom'), Gtxn[1].sender()),
    	Approve() )

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
