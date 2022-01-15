from pyteal import *

globals().update(TealType.__members__)


@Subroutine(TealType.bytes)
def numtostr(num):
    out = ScratchVar(TealType.bytes)
    i = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    n = ScratchVar(TealType.uint64)
    done = ScratchVar(TealType.uint64)
    return  Seq([
    	out.store(Bytes("             ")),
    	i.store(Int(0)),
    	digit.store(Int(0)),
    	n.store(num),
    	done.store(Int(0)),
    	While( Not( done.load() )).Do(
          Seq([
    	     digit.store(n.load() % Int(10)),
    	     out.store(SetByte(out.load(), Int(12)-i.load(), digit.load()+Int(48))),
    	     n.store(n.load() / Int(10)),
    	     If( n.load() == Int(0), done.store(Int(1))
                  ),
    	     i.store(i.load() + Int(1)) ])
       ),
    	Return( Extract(out.load(), Int(12) - i.load() + Int(1), i.load()) ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
