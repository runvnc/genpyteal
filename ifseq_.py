from pyteal import *

globals().update(TealType.__members__)


@Subroutine(TealType.none)
def foo(b):
  x = ScratchVar(TealType.uint64)
  return x.store(b)
  

def app():
    return  Seq([
    	foo(Int(10)),
    	Return( Int(1) ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
