from pyteal import Subroutine, TealType, Exp, Int, If


@Subroutine(TealType.uint64)
def exp10(x: TealType.uint64):
    return Exp(Int(10), x)


@Subroutine(TealType.uint64)
def max(a: TealType.uint64, b: TealType.uint64):
    return If(a > b, a, b)


@Subroutine(TealType.uint64)
def min(a: TealType.uint64, b: TealType.uint64):
    return If(a < b, a, b)
