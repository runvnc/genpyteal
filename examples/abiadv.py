from lib.util import *

JUNK_ASSET = 575753250

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
living_room_connects = "ESSYWD"
living_room_conn_descr = """From here you can enter the study to the east, the dining room (west), or go back outside (south)."""

study = """Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons books."""
study_connects = "WL"
study_conn_descr = "To the west is the living room."  

dining = """Dining Room
This is a small area with an old wooden table taking up most of the space. The layers of stains on the carpet are truly breathtaking.
There is a merchant here. He has his goods spread out on the table."""
dining_connects = "EL"
dining_conn_descr = "To the east is the living room."

computer = """The screen shows the following:
\033[38;2;138;226;52m\033[48;2;0;21;0m
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

sign = """
\033[38;5;2mSale!
Only 0.02 ALGO per item\033[0m

To buy an item (if using the 'avmloop' client), enter the following command:
\033[38;2;138;226;52m\033[48;2;0;21;0m
> /optin 575753250,/pay 0.02,buy 575753250 junk\033[0m
"""

@bytes
def get_connects(l):
  if l == 'Y': return yard_connects
  if l == 'L': return living_room_connects
  if l == 'S': return study_connects
  if l == 'D': return dining_connects
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
  if l == 'D': printloc(dining, dining_conn_descr, dining_connects)
  return 1

def show_inventory_():
  inv = StringArray(lgets('inventory'))
  print("You are carrying:")
  print(fgYellow)

  if lgeti('junk_count') > 0:
    print(numtostr(lgeti('junk_count')) + ' Garage Sale Junk')
  
  inv.init()
  i = 0 
  while i < inv.size:
    print(abi.String(inv[i]).value)
    i = i + 1
  print(resetColor)
  return 1

def show_junk():    
  print(numtostr( asset_bal(app_address, 0)) + " Garage Sale Junk")

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
      print(abi.String(items[i]).value)
      i = i + 1
    
  print(resetColor)

def printitem(i):
  print(fgWhite)
  if i == 'computer': print(computer)
  if i == 'note': print(note)
  if i == 'sign': print(sign)
  print(resetColor)

def exists_item(item, loc):
  if loc == 'S' and (item == 'computer' or item == 'books'):
    return True
  if loc == 'D' and item == 'sign':
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
  print(Concat(fgRed, clr('Bitcoin Maximalist ', bgWhite), fgRed, resetColor))
  print('suddenly appears. He attacks you with')
  print(Concat(clr('Nonsense', fgRed), resetColor))
  print('and runs away.')
  print(Concat(clr('You lose [10] hit points', bgRed), fgWhite, resetColor)) 
  return 1

def buy_(asset, what):  
  if find_payment(20000):
    Begin()
    SetFields({
      TxnField.type_enum: TxnType.AssetTransfer,
      TxnField.sender: app_address,
      TxnField.asset_amount: 1,
      TxnField.asset_receiver: Txn.sender,
      TxnField.xfer_asset: Txn.assets[Btoi(asset)]
    })
    Submit()
    print("You bought it.")
    lput('junk_count', asset_bal(Txn.sender, 0))
    return 1
  return 0

def find_payment(amount):
  i = 0
  found = 0
  while i < Global.group_size:
    if (Gtxn[i].sender == Txn.sender and 
        Gtxn[i].receiver == Global.current_application_address and 
        Gtxn[i].amount == amount):
      found = True
    i = i + 1
      
  return found

def find_axfer(assetid):
  i = 0
  found = 0
  while i < Global.group_size:
    if (Gtxn[i].asset_id == assetid and 
        Gtxn[i].asset_receiver == Global.current_application_address and 
        Gtxn[i].asset_amount == 1):
      found = True
    i = i + 1
      
  return found
  
def offer_(asset, what):
  if what == "junk":
    Begin()
    SetFields({
      TxnField.type_enum: TxnType.AssetTransfer,
      TxnField.sender: Global.current_application_address,
      TxnField.asset_amount: 0,
      TxnField.asset_receiver: Global.current_application_address,
      TxnField.xfer_asset: Txn.assets[asset]
    })
    Submit()   
    print("The merchant will take your junk.")
    return 1
  return 0

def use_(item:bytes):
  if arr_find(lgets('inventory'), item) == NOT_FOUND:
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
  
def take_(what:TealType.bytes):
  inv = StringArray(lgets('inventory'))
  ind = 0
  ind =  arr_find(ggets(lgets('location')+'_items'), what)
  if ind == NOT_FOUND:
    print('You do not see that here, or it is not something you can take.')
  else:  
    inv.init()
    inv.append(abi.String.encode(what))
    lput('inventory', inv.serialize())
    gput(lgets('location')+'_items', arr_del(ggets(lgets('location')+'_items'), ind))
    
    print('You take the ' + what)
  return 1

def drop_(what:TealType.bytes):
  items = StringArray(ggets(lgets('location') + '_items'))
  ind = 0
  ind = arr_find(lgets('inventory'), what) 
  if ind == NOT_FOUND:
    print('You are not carrying that.')
  else:
    lput('inventory', arr_del(lgets('inventory'), ind))
    items.init()
    items.append(abi.String.encode(what))
    #print('You dropped the ' + what)
    gput(lgets('location')+'_items', items.serialize())    
  return 1
  
def init_local_array(name):
  strarr = StringArray("")
  strarr.init()
  if name == 'inventory':
    strarr.append(abi.String.encode('note'))
  
  lput(name, strarr.serialize())

def init_global_array(name, df):
  strarr = StringArray("")
  strarr.init()
  if df != '':
    strarr.append(abi.String.encode(df))

  gput(name, strarr.serialize())


def setup_():
  lput('location', 'Y')
  lput('junk_count', 0)
  init_local_array('inventory')
  init_global_array('Y_items', '')
  init_global_array('L_items', '')
  init_global_array('S_items', 'd20')  
  init_global_array('D_items', 'sign')
  
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

def buy(optin, pay, asset, item: String ) -> abi.Uint32:
  return buy_(asset, abi.String(item).value)    

def offer(asset, item: String) -> abi.Uint32:
  return offer_(asset, abi.String(item).value)    
