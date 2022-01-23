yard = """Front Yard
You are standing in front of a house. It is white, with green trim."""
yard_connects="NL"
yard_conn_descr = "To the north is the front door."

living_room = """Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on."""
living_room_connects = "ESSY"
living_room_conn_descr = """From here you can enter the study to the east or go back outside (south)."""

study = """Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons Books."""
study_connects = "W"
study_conn_descr = "To the west is the living room."  

@bytes
def get_connects(location):
  if l == 'Y': return yard_connects
  if l == 'L': return living_room_connects
  if l == 'S': return study_connects

def move(location, direction):
  connects = ""
  connects = get_connects(location)
  i = 0
  l = 0
  l = Len(connects)
  while i < l:
    if Extract(connects, i, 1) == direction:
      App.globalPut('location', Extract(connects, i + 1, 1))
      return True
    i = i + 1
      
  return False

def printloc(descr, conn_descr, connects):
  print(descr)
  print(conn_descr)
  print(connects)

def show(l):
  if l == 'Y': printloc(yard, yard_conn_descr, yard_connects)    
  if l == 'L': printloc(living_room, living_room_conn_descr, living_room_connects)
  if l == 'S': printloc(study, study_conn_descr, study_connects)
  return 1

@staticmethod
def delete() -> Expr:
  return Approve()

def setup_():
  App.globalPut('location', 'Y')
  return 1

def look() -> Uint32:
  return show(App.globalGet('location'))

def setup() -> Uint32:
  return setup_()

