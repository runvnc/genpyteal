from pyteal import *

globals().update(TealType.__members__)

def verbatim(x):
  return x

class Senior:
  
  @verbatim
  def __init__(self, name, age):
    self.age = age
    self.name = name
  
  
  def isEligible(self):
    return ( self.age > Int(65) )
  
  
  def evalAndPrint(self):
    a = ScratchVar(TealType.uint64)
    return  Seq(
    	a.store(Int(10)),
    	If( self.isEligible(), 
          Log(Concat(self.name,Concat(Bytes(" is eligible. "),Itob(a.load()))))
        , 
          Log(Concat(self.name,Bytes(" is too young.")))
       ) )
  
  
  
def app():
    mary = Senior(Bytes('Mary'), Int(62))
    tom = Senior(Bytes('Tom'), Int(75))
    return  Seq(
    	mary.evalAndPrint(),
    	tom.evalAndPrint(),
    	Return( Int(1) ) )


if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=7))
