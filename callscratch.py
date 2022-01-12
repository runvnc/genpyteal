def int(x):
    return x

# ii.parent.replace(ii.parent.dumps().replace('@int','@Subroutine(uint64)'))
    
def intvar():
    return ScratchVar(uint64)

@int
def g(x):
    return 3

@Subroutine(uint64)
def f(n):
    s = intvar()
    s.store(g(n))
    return 1

@Subroutine(uint64)
def teal():
    retval = intvar()
    retval.store(f(30))
    return retval.load()
