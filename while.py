from pyteal import *

globals().update(TealType.__members__)

def teal():
    totalFees = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    return  Seq([
    	totalFees.store(Int(0)),
    	i.store(Int(0)),
    	While( i.load() < Global.group_size()).Do(
          Seq([
    	     totalFees.store(totalFees.load() + Gtxn[i.load()].fee()),
    	     i.store(i.load() + Int(1)) ])
       ),
    	Return( Int(1) ) ])

if __name__ == "__main__":
    print(compileTeal(teal(), mode=Mode.Application, version=5))
