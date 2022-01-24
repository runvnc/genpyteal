from pyteal import *

globals().update(TealType.__members__)

hash_ = ScratchVar(bytes, 40)
s1 = ScratchVar(bytes)
ts = ScratchVar(bytes)
ts.store(Itob( Global.latest_timestamp() ) )
cm = ScratchVar(bytes)
cm.store( Concat(Txn.tx_id(), ts.load()) )
hash_.store( Sha256 ( cm.load() ) )

rndcnt = ScratchVar(uint64, 42)
rndcnt.store(Int(0))

#bigRand = Btoi( Extract( Bytes(hash.load()), Int(rndcnt), 7+Int(rndcnt)) )
@Subroutine(uint64)
def rnd(mn, mx):
    hash = ScratchVar(bytes, 40)
    rndcnt = ScratchVar(TealType.uint64, 42)
    somebytes = ScratchVar(TealType.bytes)
    bigRand = ScratchVar(TealType.uint64)
    
    return  Seq([
      rndcnt.store(Int(0)),
    	bigRand.store(Int(0)),
    	somebytes.store(Bytes("")),
    	somebytes.store(Extract( hash_.load(), rndcnt.load(), Int(7) + rndcnt.load() ) ),
    	bigRand.store( Btoi( somebytes.load() ) ),
    	rndcnt.store(rndcnt.load() + Int(1)),
    	Return( mn + bigRand.load() % (mx - mn + Int(1)) ) ])



@Subroutine(TealType.bytes)
def numtostr(num):
    done = ScratchVar(TealType.uint64)
    n = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    out = ScratchVar(TealType.bytes)
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
