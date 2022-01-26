from lib import util

fgGreen = "\033[38;5;2m"
fgYellow = "\033[38;5;11m"
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
  l = Len(connects)
  while i < l:
    if Extract(connects, i, 1) == direction:
      App.localPut(0, 'location', Extract(connects, i + 1, 1))
      d = show(App.localGet(0, 'location'))
      return True
    i = i + 2
      
  return False

def printloc(descr, conn_descr, connects):
  print(fgWhite)
  print(descr)
  
  print(fgYellow)
  print(conn_descr)
  
  print(fgGreen)
  print(connects)

  print(resetColor)

def show(l):
  if l == 'Y': printloc(yard, yard_conn_descr, yard_connects)    
  if l == 'L': printloc(living_room, living_room_conn_descr, living_room_connects)
  if l == 'S': printloc(study, study_conn_descr, study_connects)
  return 1

def inventory_():  
  print("You are carrying:")
  print(fgYellow)
  print(App.localGet(Txn.sender, 'inventory'))
  print(resetColor)
  return 1

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
  return util.rnd(1, 20)

def examine_(i):
  if exists_item(i, App.localGet(Txn.sender, 'location')):    
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
    print("[ " + util.numtostr(roll) + " ]")
    print(resetColor)
  else:
    print("You can't use that.")
  return 1
  
def take_(what):
  curr = ""
  curr = App.localGet(Txn.sender, 'inventory')
  App.localPut(Txn.sender, 'inventory', curr + "\n" + what)
  return 1


def setup_():
  App.localPut(0, 'location', 'Y')
  App.localPut(0, 'inventory', "note")
  return 1

def look() -> abi.Uint32:
  return show(App.localGet(0, 'location'))

def setup() -> abi.Uint32:
  return setup_()

def move(dir: String) -> abi.Uint32:
  return move_(App.localGet(0, 'location'), dir)

def take(what: String) -> abi.Uint32:
  return take_(what)

def inventory() -> Uint32:
  return inventory_()

def examine(what: String) -> abi.Uint32:
  return examine_(what)

def use(item: String) -> abi.Uint32:
  return use_(item)
    
