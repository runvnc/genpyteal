from lib.util import *


def show_inventory_():
  inv = StringArray(lget('inventory'))
  inv.init()
  i = 0  
  while i < inv.size:
    print(inv[i])
    i = i + 1
  return 1
  
def init() -> abi.Uint32:
  inv = StringArray("")
  inv.init()
  lput('inventory', inv.serialize())
  1

def get_inventory() -> StringArray:
  return lget('inventory')

def pickup(item: String) -> abi.Uint32:
  inv = StringArray(lget('inventory'))
  inv.init()
  inv.append(item)
  return show_inventory_()

def show_inventory() -> abi.Uint32:
  return show_inventory_()

