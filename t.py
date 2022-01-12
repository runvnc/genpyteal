from pyteal import *

globals().update(TealType.__members__)

@Subroutine(uint64)
def g(x):
    return Int(3)

@Subroutine(TealType.none)
def f(n):
    s = ScratchVar(TealType.uint64)
    s.store(g(n))

@Subroutine(uint64)
def teal():
    x = ScratchVar(TealType.uint64)
    retval = ScratchVar(TealType.uint64)
    return Seq([x.store(f(Int(30))),
    retval.store(Int(100)),
    Return(retval.load())])

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
