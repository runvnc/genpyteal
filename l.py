
import json
from typing import Tuple

from pyteal import *

from pytealutils.applications import ABIMethod, DefaultApprove
from pytealutils import abi

globals().update(TealType.__members__)


from lib import util




fgGreen = Bytes("\033[38;5;2m")


fgYellow = Bytes("\033[38;5;11m")


fgWhite = Bytes("\033[38;5;15m")


resetColor = Bytes("\033[0m")




yard = Bytes("Front Yard\nYou are standing in front of a house. It is white, with green trim.")


yard_connects = Bytes("NL")


yard_conn_descr = Bytes("To the north is the front door.")




living_room = Bytes("""Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on.""")


living_room_connects = Bytes("ESSY")


living_room_conn_descr = Bytes("""From here you can enter the study to the east or go back outside (south).""")




study = Bytes("""Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons Books.""")


study_connects = Bytes("WL")


study_conn_descr = Bytes("To the west is the living room.")
  



computer = Bytes("""The screen shows the following:
\033[38;2;138;226;52m[48;2;0;21;0m
A>dir                             
A: MOVCPM   COM  
A: ASMAVM   COM  
A: CHIP8    COM  
\033[0m
""")




note = Bytes("""
Welcome to 'Mini-Adventure'. For a list of commands, type /menu.
You probably already knew that though, or you would not have got to this point.
""")





@Subroutine(TealType.bytes)
def get_connects(l):
    return  Seq(
    	If( l == Bytes('Y'), Return( yard_connects )
         ),
    	If( l == Bytes('L'), Return( living_room_connects )
         ),
    	If( l == Bytes('S'), Return( study_connects )
         ),
    	Return( Bytes('') ) )



@Subroutine(uint64)
def move_(location, direction):
    d = ScratchVar(TealType.uint64)
    l = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    connects = ScratchVar(TealType.bytes)
    return  Seq(
    	connects.store(Bytes("")),
    	connects.store(get_connects(location)),
    	i.store(Int(0)),
    	l.store(Int(0)),
    	d.store(Int(0)),
    	l.store(Len(connects.load())),
    	While( i.load() < l.load()).Do(
          Seq(
    	     If( Extract(connects.load(), i.load(), Int(1)) == direction, 
                     Seq(
    	                App.localPut(Int(0), Bytes('location'), Extract(connects.load(), i.load() + Int(1), Int(1))),
    	                d.store(show(App.localGet(Int(0), Bytes('location')))),
    	                Return( Int(1) ) )
              ),
    	     i.store(i.load() + Int(2)) )
       ),
    	Return( Int(0) ) )



@Subroutine(TealType.none)
def printloc(descr, conn_descr, connects):
    return  Seq(
    	Log(fgWhite),
    	Log(descr),
    	Log(fgYellow),
    	Log(conn_descr),
    	Log(fgGreen),
    	Log(connects),
    	Log(resetColor) )



@Subroutine(uint64)
def show(l):
    return  Seq(
    	If( l == Bytes('Y'), printloc(yard, yard_conn_descr, yard_connects)    
         ),
    	If( l == Bytes('L'), printloc(living_room, living_room_conn_descr, living_room_connects)
         ),
    	If( l == Bytes('S'), printloc(study, study_conn_descr, study_connects)
         ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def inventory_():
    return  Seq(
    	Log(Bytes("You are carrying:")),
    	Log(fgYellow),
    	Log(App.localGet(Txn.sender(), Bytes('inventory'))),
    	Log(resetColor),
    	Return( Int(1) ) )



@Subroutine(TealType.none)
def printitem(i):
    return  Seq(
    	Log(fgWhite),
    	If( i == Bytes('computer'), Log(computer)
         ),
    	If( i == Bytes('note'), Log(note)
         ),
    	Log(resetColor) )



@Subroutine(uint64)
def exists_item(item, loc):
    return  Seq(
    	If( And( loc == Bytes('S'), (Or( item == Bytes('computer'), item == Bytes('books') )) ), 
          Return( Int(1) )
         ),
    	If( item == Bytes('note'), 
          Return( Int(1) )
         ),
    	Return( Int(0) ) )



@Subroutine(uint64)
def rolld20():
  return ( util.rnd(Int(1), Int(20)) )


@Subroutine(uint64)
def examine_(i):
    s = ScratchVar(TealType.bytes)
    return  Seq(
    	If( exists_item(i, App.localGet(Txn.sender(), Bytes('location'))),     
          printitem(i)
        , 
            Seq(
    	       s.store(Bytes("")),
    	       s.store(i),
    	       s.store(Concat(Bytes("There is no "),s.load())),
    	       s.store(Concat(s.load(),Bytes(" here."))),
    	       Log(s.load()) )
       ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def use_(item):
    roll = ScratchVar(TealType.uint64)
    return  Seq(
    	If( Or( item == Bytes('die'), Or( item == Bytes('dice'), item == Bytes('d20') ) ), 
            Seq(
    	       Log(Bytes("Rolling d20...")),
    	       Log(fgYellow),
    	       roll.store(Int(0)),
    	       roll.store(rolld20()),
    	       Log(Concat(Bytes("[ "),Concat(util.numtostr(roll.load()),Bytes(" ]")))),
    	       Log(resetColor) )
        , 
          Log(Bytes("You can't use that."))
         ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def take_(what):
    curr = ScratchVar(TealType.bytes)
    return  Seq(
    	curr.store(Bytes("")),
    	curr.store(App.localGet(Txn.sender(), Bytes('inventory'))),
    	App.localPut(Txn.sender(), Bytes('inventory'), Concat(curr.load(),Concat(Bytes("\n"),what))),
    	Return( Int(1) ) )



@Subroutine(uint64)
def setup_():
    return  Seq(
    	App.localPut(Int(0), Bytes('location'), Bytes('Y')),
    	App.localPut(Int(0), Bytes('inventory'), Bytes("note")),
    	Return( Int(1) ) )



class ABIApp(DefaultApprove):

  @staticmethod
  @ABIMethod
  def look() -> abi.Uint32:
    return ( show(App.localGet(Int(0), Bytes('location'))) )

  

  @staticmethod
  @ABIMethod
  def setup() -> abi.Uint32:
    return ( setup_() )

  

  @staticmethod
  @ABIMethod
  def move(dir: String) -> abi.Uint32:
    return ( move_(App.localGet(Int(0), Bytes('location')), dir) )

  

  @staticmethod
  @ABIMethod
  def take(what: String) -> abi.Uint32:
    return ( take_(what) )

  

  @staticmethod
  @ABIMethod
  def inventory() -> abi.Uint32:
    return ( inventory_() )

  

  @staticmethod
  @ABIMethod
  def examine(what: String) -> abi.Uint32:
    return ( examine_(what) )

  

  @staticmethod
  @ABIMethod
  def use(item: String) -> abi.Uint32:
    return ( use_(item) )




if __name__ == "__main__":
  app = ABIApp()

  with open("interface.json", "w") as f:
    f.write(json.dumps(app.get_interface().dictify(), indent=4))

  print(compileTeal(app.handler(), mode=Mode.Application, version=5, assembleConstants=True))
  
