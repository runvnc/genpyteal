def Seq(l):
    map(lambda x: x(), l)

def blah(n):
    print("blah",n)


def fn():
    Seq([blah(100),
    blah(200)])


fn()
