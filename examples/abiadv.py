from lib.util import *

fgGreen = "\033[38;5;2m"
fgYellow = "\033[38;5;11m"
fgPurple = "\033[38;5;35m"
fgWhite = "\033[38;5;15m"
resetColor = "\033[0m"

yard = "Front Yard\nYou are standing in front of a house. It is white, with green trim."
yard_connects = "NL"
yard_conn_descr = "To the north is the front door."

living_room = """Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on."""
living_room_connects = "ESSY"
living_room_conn_descr = """From here you can enter the study to the east or go back outside (south)."""

study = """Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons Books."""
study_connects = "WL"
study_conn_descr = "To the west is the living room."  

computer = """The screen shows the following:
\033[38;2;138;226;52m[48;2;0;21;0m
A>dir                             
A: MOVCPM   COM  
A: ASMAVM   COM  
A: CHIP8    COM  
\033[0m
"""

note = """
Welcome to 'Mini-Adventure'. For a list of commands, type /menu.
You probably already knew that though, or you would not have got to this point.
"""

@bytes
def get_connects(l):
  if l == 'Y': return yard_connects
  if l == 'L': return living_room_connects
  if l == 'S': return study_connects
  return ''

def move_(location, direction):
  connects = ""
  connects = get_connects(location)
  i = 0
  l = 0
  d = 0
  while i < Len(connects):
    if Extract(connects, i, 1) == direction:
      lput('location', Extract(connects, i + 1, 1))
      d = show(lgets('location'))
      return True
    i = i + 2
      
  return False

def printloc(descr, conn_descr, connects):
  print(fgWhite)
  print(descr)
  
  print(fgYellow)
  print(conn_descr)

  show_at_location_()
  
  print(fgGreen)
  print(connects)

  print(resetColor)

def show(l):
  if l == 'Y': printloc(yard, yard_conn_descr, yard_connects)    
  if l == 'L': printloc(living_room, living_room_conn_descr, living_room_connects)
  if l == 'S': printloc(study, study_conn_descr, study_connects)
  return 1


def show_inventory_():
  inv = StringArray(lgets('inventory'))
  print("You are carrying:")
  print(fgYellow)

  inv.init()
  i = 0 
  while i < inv.size:
    print(abi.String(inv[i]).value)
    i = i + 1
  print(resetColor)
  return 1

def show_at_location_():
  items = StringArray(lgets(lgets('location') + '_items'))
  print('You see the following items here:')
  print(fgPurple)
  items.init()
  i = 0 
  while i < items.size:
    print(abi.String(items[i]).value)
    i = i + 1
  
  print(resetColor)

def printitem(i):
  print(fgWhite)
  if i == 'computer': print(computer)
  if i == 'note': print(note)
  print(resetColor)

def exists_item(item, loc):
  if loc == 'S' and (item == 'computer' or item == 'books'):
    return True
  if item == 'note':
    return True
  return False

def rolld20():
  return rnd(1, 20)

def examine_(i):
  if exists_item(i, lgets('location')):    
    printitem(i)
  else:
    s = ""
    s = i
    s = "There is no " + s
    s = s + " here."
    print(s)
  return 1

def use_(item):
  if item == 'die' or item == 'dice' or item == 'd20':
    print("Rolling d20...")
    print(fgYellow)
    roll = 0
    roll = rolld20()
    print("[ " + numtostr(roll) + " ]")
    print(resetColor)
  else:
    print("You can't use that.")
  return 1

def takeable_at(item:bytes):
  if arr_find(lgets(lgets('location')+'_items'), item) != 999:
    return True
  else:
    return False
  
def take_(what:TealType.bytes):
  inv = StringArray(lgets('inventory'))
  if not takeable_at(what):
    print('You do not see that here, or it is not something you can take.')
  else:  
    inv.init()
    inv.append(String(what))
    lput('inventory', inv.serialize())
    print('You take the ' + what)
  return 1

def drop_(what):
  inv = StringArray(lgets('inventory'))
  inv.init()
  if not arr_find(inv, what):
    print('You are not carrying that.')
  else:
    arr_del(inv, what)
    arrname = lgets('location') + '_items'
    items = StringArray(lgets(arrname))
    items.init()
    items.append(what)
    print('You dropped the ' + what + '.')
  return 1
  
def init_local_array(name):
  strarr = StringArray("")
  strarr.init()
  lput(name, strarr.serialize())

def init_global_array(name):
  strarr = StringArray("")
  strarr.init()
  gput(name, strarr.serialize())

def setup_():
  lput('location', 'Y')
  init_global_array('inventory')
  init_global_array('Y_items')
  init_global_array('L_items')
  init_global_array('S_items')
  init_global_array('D_items')
  
  return 1

def look() -> abi.Uint32:
  return show(lgets('location'))

def setup() -> abi.Uint32:
  return setup_()

def move(dir: String) -> abi.Uint32:
  return move_(lgets('location'), dir)

def take(what: String) -> abi.Uint32:
  return take_(what)

def inventory() -> StringArray:
  return lgets('inventory')

def examine(what: String) -> abi.Uint32:
  return examine_(what)

def use(item: String) -> abi.Uint32:
  return use_(item)
    
