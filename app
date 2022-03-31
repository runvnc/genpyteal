from pyteal import *

globals().update(TealType.__members__)

#L1
@Subroutine(TealType.none)
def foo(b): #L2
    x = ScratchVar(TealType.uint64)
    return x.store(b)
def app(): #L5
    return  Seq(
    	foo(Int(10)),
    	If( Int(1) == Int(1), 
             If( Int(10)<Int(3), 
                      Return( Int(1) ) #L8
                   )
        , 
          Return( Int(0) ) #L10
       ) )

if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=5))
