from pyteal import *

globals().update(TealType.__members__)

@Subroutine(uint64)
def g(x):
    return Int(3)

@Subroutine(uint64)
def f(n):
    return g(n)

def teal():
    x = ScratchVar(TealType.uint64)
    name = ScratchVar(TealType.bytes)
    retval = ScratchVar(TealType.uint64)
    return Seq([
    x.store(f(Int(30))),
    name.store(Bytes("Bob")),
    Log(name.load()),
    retval.store(Int(100)),
    Return(retval.load())])

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
