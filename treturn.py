@Subroutine(TealType.uint64)
def g(x):
    return Int(30)

@Subroutine(TealType.uint64)
def f(n):
    g(Int(100+n))
    return Int(1)

def teal():
    return f(Int(30))
    #return Int(1)
