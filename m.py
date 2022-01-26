from pyteal import *

globals().update(TealType.__members__)

from lib import util

@Subroutine(uint64)
def proc(n):
  return ( n * Int(2) )

@Subroutine(uint64)
def acceptable(n, target):
    return If( n >= target,
            Seq([
               Log(Concat(Bytes("Acceptable. Diff is "),util.numtostr(n - target))),
               Return( Int(1) ) ])

        ,
          Return( Int(0) )

       )


def app():
    i = ScratchVar(TealType.uint64)
    total = ScratchVar(TealType.uint64)
    return  Seq([
        total.store(Int(1)),
        i.store(Int(0)),
        While( Not( acceptable(total.load(), Btoi(Txn.application_args[0])) )).Do(
          Seq([
             total.store(proc(total.load())),
             i.store(Int(1)) ])
       ),
        Return( i.load() ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
    
