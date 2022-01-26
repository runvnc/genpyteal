
import json
from typing import Tuple

from pyteal import *

from pytealutils.applications import ABIMethod, DefaultApprove
from pytealutils import abi

globals().update(TealType.__members__)


from lib.util import *




@Subroutine(TealType.none)
def show_inventory():
    i = ScratchVar(TealType.uint64)
    inv = StringArray(App.localGet(Int(0), Bytes('inventory')))
    return  Seq([
    	inv.init(),
    	i.store(Int(0)),
    	While( i.load() < inv.size.load()).Do(
          Seq([
    	     Log(inv[i.load()]),
    	     i.store(i.load() + Int(1)) ])
     ) ])



class ABIApp(DefaultApprove):

  @staticmethod
  @ABIMethod
  def init() -> abi.Uint32:
      inv = StringArray(Bytes(""))
      return  Seq([
    	  inv.init(),
    	  App.localPut(Int(0), Bytes('inventory'), inv.serialize()),
    	  Int(1) ])


  

  @staticmethod
  @ABIMethod
  def get_inventory() -> StringArray:
    return ( App.localGet(Int(0), Bytes('inventory')) )

  

  @staticmethod
  @ABIMethod
  def pickup(item: String) -> abi.Uint32:
      inv = StringArray(App.localGet(Int(0), Bytes('inventory')))
      return  Seq([
    	  inv.init(),
    	  inv.append(item),
    	  show_inventory(),
    	  Int(1) ])



if __name__ == "__main__":
  app = ABIApp()

  with open("interface.json", "w") as f:
    f.write(json.dumps(app.get_interface().dictify(), indent=4))

  print(compileTeal(app.handler(), mode=Mode.Application, version=5, assembleConstants=True))
  
