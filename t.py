from pyteal import *

globals().update(TealType.__members__)

def intvar():
    return ScratchVar(uint64)

@Subroutine(uint64)
def g(x):
    return Int(3)

@Subroutine(uint64)
def f(n):
    s = intvar()
    return Seq([s.store(g(n)),
    Return(Int(1))])

@Subroutine(uint64)
def teal():
    retval = intvar()
    return Seq([retval.store(f(Int(30))),
    Return(retval.load())])

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
