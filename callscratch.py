from pyteal import *

@Subroutine(TealType.uint64)
def g(x):
    return Int(3)

@Subroutine(TealType.uint64)
def f(n):
    s = ScratchVar(TealType.uint64)
    s.store(g(n))
    return Int(1)

@Subroutine(TealType.uint64)
def teal():
    retval = ScratchVar(TealType.uint64)
    retval.store(f(Int(30)))
    return retval.load()

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
