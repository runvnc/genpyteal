from pyteal import *

globals().update(TealType.__members__)

def app():
    name = ScratchVar(TealType.bytes)
    age = ScratchVar(TealType.uint64)
    return  Seq([
    	name.store(Bytes("")),
    	name.store(Txn.application_args[0]),
    	age.store(Btoi(Txn.application_args[1])),
    	If( age.load() > Int(65), 
          Log(name.load() + Bytes(" is at retirement age."))
        , 
          Log(name.load() + Bytes(" is still young."))
         ),
    	Return( Int(1) ) ])

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
