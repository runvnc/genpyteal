from pyteal import *

globals().update(TealType.__members__)


@Subroutine(TealType.bytes)
def numtostr(n):
    out = ScratchVar(TealType.bytes)
    i = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    return  Seq([
    	out.store(Bytes("             ")),
    	i.store(Int(0)),
    	digit.store(Int(0)),
    	While( Int(1)).Do(
          Seq([
    	     digit.store(n.load() % Int(10)),
    	     out.store(SetByte(out, Int(2)-i.load(), digit.load()+Int(48))),
    	     n.store(n.load() / Int(10)),
    	     If( n.load() == Int(0), 
                   Return( out.load() )
                  ),
    	     i.store(i.load() + Int(1)) ])
     ) ])


def app():
    return  Seq([
    	Log(numtostr(Int(45))),
    	Return( Int(1) ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
