from pyteal import *

globals().update(TealType.__members__)

#def put(n):
#  Log("Hello")

@Subroutine(TealType.uint64)
def foo(b):
  x = ScratchVar(TealType.uint64)
  return Seq([ x.store(Int(9)),
  Return(x.load())])

  #def fn1(n):
  #  foo(n+2)
  #  foo(n-2)

def app():
    n = ScratchVar(TealType.uint64)
    return  Seq([
    	n.store(foo(Int(10))),
    	Return( Int(1) ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
