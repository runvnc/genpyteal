from lib.util import *

fgGreen = "\033[38;5;2m"
fgYellow = "\033[38;5;11m"
fgPurple = "\033[38;5;35m"
fgWhite = "\033[38;5;15m"
fgRed = '\033[38;5;31m'
bgWhite = '\033[48;2;250;250;250m'
bgRed = '\033[48;2;250;0;0m'
resetColor = "\033[0m\033[48;2;0;0;0m"

yard = "Front Yard\nYou are standing in front of a house. It is white, with green trim."
yard_connects = "NL"
yard_conn_descr = "To the north is the front door."

living_room = """Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on."""
living_room_connects = "ESSY"
living_room_conn_descr = """From here you can enter the study to the east or go back outside (south)."""

study = """Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons books."""
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
  print("Trying to move " + direction)
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
  items = StringArray(ggets(lgets('location') + '_items'))
  items.init()
  if items.size == 0:
    n = 0
  else:
    print('You see the following items here:')
    print(fgPurple)
    
    i = 0 
    while i < items.size:
      print(items[i])
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

def encounter():
  print('A')
  print(clr('Bitcoin Maximalist ',Concat(fgRed, bgWhite)))
  print(clr('suddenly appears and attacks you with',resetColor))
  print(clr('Nonsense', fgRed))
  #print(B(bgRed) + B(fgWhite) + 'You lose [10] hit points' + B(resetColor))
  return 1

def use_(item:bytes):
  if arr_find(lgets('inventory'), item) == 999:
    print('You are not carrying that.')
    return 1

  if item == 'die' or item == 'dice' or item == 'd20':
    print("Rolling d20...")
    print(fgYellow)
    roll = 0
    roll = rolld20()
    print("[ " + numtostr(roll) + " ]")
    print(resetColor)
    if roll < 10:
      return encounter()
  else:
    print("You can't use that.")
  return 1

def takeable_at(item:bytes):
  if arr_find(ggets(lgets('location')+'_items'), item) != 999:
    return True
  else:
    return False
  
def take_(what:TealType.bytes):
  inv = StringArray(lgets('inventory'))
  if not takeable_at(what):
    print('You do not see that here, or it is not something you can take.')
  else:  
    inv.init()
    inv.append(abi.String.encode(what))
    lput('inventory', inv.serialize())
    print('You take the ' + what)
  return 1

def drop_(what:TealType.bytes):
  items = StringArray(ggets(lgets('location') + '_items'))
  if not arr_find(lgets('inventory'), what):
    print('You are not carrying that.')
  else:
    lput('inventory', arr_del(lgets('inventory'), what))
    items.init()
    items.append(abi.String.encode(what))
    print('You dropped the ' + what)
    gput(lgets('location')+'_items', items.serialize())    
  return 1
  
def init_local_array(name):
  strarr = StringArray("")
  strarr.init()
  #if name == 'inventory':
  #  strarr.append('note')
  
  lput(name, strarr.serialize())

def init_global_array(name):
  strarr = StringArray("")
  strarr.init()
  if name == 'S_items':
    strarr.append(abi.String.encode('d20'))

  gput(name, strarr.serialize())

def setup_():
  lput('location', 'Y')
  init_local_array('inventory')
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
  return move_(lgets('location'), abi.String(dir).value)

def take(what: String) -> abi.Uint32:
  return take_(abi.String(what).value)

def drop(what: String) -> abi.Uint32:
  return drop_(abi.String(what).value)

def inventory() -> StringArray:
  return lgets('inventory')

def examine(what: String) -> abi.Uint32:
  return examine_(abi.String(what).value)

def use(item: String) -> abi.Uint32:
  return use_(abi.String(item).value)
    
