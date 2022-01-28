from pyteal import *

globals().update(TealType.__members__)

from typing import Tuple

from pyteal import *

from pytealutils import abi

from .libex import *

StringArray = abi.DynamicArray[abi.String]

NOT_FOUND = Int(999)


@Subroutine(TealType.bytes)
def clr(s, ansi):
  return ( Concat(ansi, s) )

@Subroutine(uint64)
def arr_find(str_arr_bytes:bytes, item:bytes):
    i = ScratchVar(TealType.uint64)
    str_arr = StringArray(str_arr_bytes)
    return  Seq(
    	str_arr.init(),
    	i.store(Int(0)),
    	While( i.load() < str_arr.size.load()).Do(
          Seq(
    	     If( str_arr[i.load()] == abi.String.encode(item), 
                   Return( i.load() )
                  ),
    	     i.store(i.load() +Int(1)) )
       ),
    	Return( NOT_FOUND ) )



@Subroutine(TealType.bytes)
def arr_del(str_arr_bytes, index_to_remove):
    i = ScratchVar(TealType.uint64)
    str_arr = StringArray(str_arr_bytes)
    new_arr = StringArray(Bytes(""))
    return  Seq(
    	new_arr.init(),
    	str_arr.init(),
    	i.store(Int(0)),
    	While( i.load() < index_to_remove).Do(
          Seq(
    	     new_arr.append(str_arr[i.load()]),
    	     i.store(i.load() + Int(1)) )
       ),
    	i.store(i.load() + Int(1)),
    	While( i.load() < str_arr.size.load()).Do(
          Seq(
    	     new_arr.append(str_arr[i.load()]),
    	     i.store(i.load() + Int(1)) )
       ),
    	Return( new_arr.serialize() ) )


@Subroutine(uint64)
def rnd(min_, max_):
    bigRand = ScratchVar(TealType.uint64)
    rndcnt = ScratchVar(TealType.uint64)
    hash_ = ScratchVar(TealType.bytes)
    return  Seq(
    	hash_.store(Bytes("")),
    	rndcnt.store(Int(0)),
    	rndcnt.store(App.globalGet(Bytes('rndcnt'))),
    	hash_.store(Sha256(Concat(Txn.tx_id(), Itob(Global.latest_timestamp())))),
    	bigRand.store(Btoi(Extract(hash_.load() ,rndcnt.load(), Int(7))) + Global.latest_timestamp() % Int(100000)),
    	rndcnt.store(rndcnt.load() + Int(1)),
    	App.globalPut(Bytes('rndcnt'), rndcnt.load()),
    	Return( min_ + bigRand.load() % (max_ - min_ + Int(1)) ) )



@Subroutine(TealType.bytes)
def numtostr(num):
    done = ScratchVar(TealType.uint64)
    n = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    out = ScratchVar(TealType.bytes)
    return  Seq(
    	out.store(Bytes("             ")),
    	i.store(Int(0)),
    	digit.store(Int(0)),
    	n.store(num),
    	done.store(Int(0)),
    	While( Not( done.load() )).Do(
          Seq(
    	     digit.store(n.load() % Int(10)),
    	     out.store(SetByte(out.load(), Int(12)-i.load(), digit.load()+Int(48))),
    	     n.store(n.load() / Int(10)),
    	     If( n.load() == Int(0), done.store(Int(1))
                  ),
    	     i.store(i.load() + Int(1)) )
       ),
    	Return( Extract(out.load(), Int(12) - i.load() + Int(1), i.load()) ) )

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
