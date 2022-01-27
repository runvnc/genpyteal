from lib.util import *

def show_inventory_():
  inv = StringArray(lgets('inventory'))
  inv.init()
  i = 0  
  while i < inv.size:
    print(inv[i])
    i = i + 1
  return 1

def pickup_(item):
  inv = StringArray(lgets('inventory'))
  inv.init()
  inv.append(item)
  lput('inventory', inv.serialize())
  return show_inventory_()

def init_():
  inv = StringArray("")
  inv.init()
  lput('inventory', inv.serialize())
  return 1
  
def init() -> abi.Uint32:
  return init_()

def get_inventory() -> StringArray:
  return lgets('inventory')

def pickup(item: String) -> abi.Uint32:
  return pickup_(item)

def show_inventory() -> abi.Uint32:
  return show_inventory_()

