from pyteal import *

def g(x):
    Return(Int(30))

def f(n):
    return Seq([g(100+n),
    Return(Int(1))])


def teal():
    return Return(f(30))
    #return Int(1)

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
