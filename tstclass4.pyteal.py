from pyteal import *

globals().update(TealType.__members__)

class Senior  


    @verbatim
    def xini(name, age):
    self.age_ = age
    self.name_ = name


    def init(self):
      self.name = ScratchVar(TealType.uint64)
      self.age = ScratchVar(TealType.uint64)
      return  Seq(
      	self.age.store(Int(self.age_)),
      	self.name.store(Bytes(self.name_)) )

    def isEligible(self):
    return ( self.age > Int(65) )


    def evalAndPrint(self):
      return If( self.isEligible(), 
            Log(Concat(self.name,Bytes(" is eligible.")))
          , 
            Log(Concat(self.name,Bytes(" is too young.")))
      
      
         )




def app():
    tom = ScratchVar(TealType.bytes)
    mary = ScratchVar(TealType.bytes)
    return  Seq(
    	mary.store(Senior(Bytes('Mary'), Int(62))),
    	mary.load().init(),
    	tom.store(Senior(Bytes('Tom'), Int(75))),
    	tom.load().init(),
    	mary.load().evalAndPrint(),
    	tom.load().evalAndPrint(),
    	Return( Int(1) ) )


if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=7))
