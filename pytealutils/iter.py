from pyteal import ScratchVar, Int, For, Expr, TealType, Subroutine


@Subroutine(TealType.none)
def range(n: TealType.uint64, method: Expr) -> Expr:
    i = ScratchVar()

    init = i.store(0)
    cond = i.load() < n
    iter = i.store(i.load() + Int(1))

    return For(init, cond, iter).Do(method)
