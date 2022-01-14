from pyteal import *

globals().update(TealType.__members__)


sum = 1

@Subroutine(TealType.none)
def put(n,m):
  print(n,m)

@Subroutine(TealType.none)
def foo(b):
  put(sum, b)  

@Subroutine(TealType.none)
def fn1(n):
    return  Seq([
    	foo(n+Int(2)),
    	foo(n-Int(2)) ])


def app():
  return If( Int(1) == Int(1), 
      Return( Int(1) )
    , 
      Return( Int(0) )
   )
   
if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
