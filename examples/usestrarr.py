from lib.util import *

def show_inventory():
  inv = StringArray(App.localGet(0, 'inventory'))
  i = 0
  while i < inv.size:
    print(inv[i])
    i = i + 1

def init() -> abi.Uint32:
  inv = StringArray("")
  App.localPut(0, 'inventory', inv.serialize())
  1

def get_inventory() -> StringArray:
  return App.localGet(0, 'inventory')

def pickup(item: String) -> abi.Uint32:
  inv = StringArray(App.localGet(0, 'inventory'))
  inv.init()
  inv.append(item)
  show_inventory()
  1

