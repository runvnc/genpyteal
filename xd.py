
import json
from typing import Tuple
from pyteal import *
from pytealutils.applications import ABIMethod
from pytealutils.applications import DefaultApprove
from pytealutils import abi


#import json
#from typing import Tuple

#from pyteal import *

#from pytealutils.applications import ABIMethod, DefaultApprove

#qglobals().update(TealType.__members__)


from lib import util

StringArray = abi.DynamicArray[abi.String]



#@Subroutine(uint64)
#def order_():
#  return ( Int(1) )


class ABIApp(DefaultApprove):

  @staticmethod
  @ABIMethod
  def order(traits: util.StringArray) -> abi.Uint32:
      i = ScratchVar(TealType.uint64)
      return Seq(        
    	  i.store(Int(0)),
    	  While( i.load() < traits.size.load()).Do(
            Seq([
    	       Log(traits[i.load()]),
    	       i.store(i.load() + Int(1)) ])
         ),
     	  i.load() )



if __name__ == "__main__":
  app = ABIApp()

  with open("interface.json", "w") as f:
    f.write(json.dumps(app.get_interface().dictify(), indent=4))

  print(compileTeal(app.handler(), mode=Mode.Application, version=5, assembleConstants=True))
  
