
import json
from typing import Tuple

from pyteal import *

from pytealutils.applications import ABIMethod, DefaultApprove
from pytealutils import abi

globals().update(TealType.__members__)


from lib.util import *




JUNK_ASSET = 575753250




fgGreen = Bytes("\033[38;5;2m")


fgYellow = Bytes("\033[38;5;11m")


fgPurple = Bytes("\033[38;5;35m")


fgWhite = Bytes("\033[38;5;15m")


fgRed = Bytes('\033[38;5;31m')


bgWhite = Bytes('\033[48;2;250;250;250m')


bgRed = Bytes('\033[48;2;250;0;0m')


resetColor = Bytes("\033[0m\033[48;2;0;0;0m")




yard = Bytes("Front Yard\nYou are standing in front of a house. It is white, with green trim.")


yard_connects = Bytes("NL")


yard_conn_descr = Bytes("To the north is the front door.")




living_room = Bytes("""Living Room
This is a small living room with a carpet that should have been replaced 15 years ago. There is a beat-up couch to sit on.""")


living_room_connects = Bytes("ESSYWD")


living_room_conn_descr = Bytes("""From here you can enter the study to the east, the dining room (west), or go back outside (south).""")




study = Bytes("""Study
There is an Ohio Scientific computer here from the late 1970s. A rickety bookshelf contains some old Dungeons & Dragons books.""")


study_connects = Bytes("WL")


study_conn_descr = Bytes("To the west is the living room.")
  



dining = Bytes("""Dining Room
This is a small area with an old wooden table taking up most of the space. The layers of stains on the carpet are truly breathtaking.
There is a merchant here. He has his goods spread out on the table.""")


dining_connects = Bytes("EL")


dining_conn_descr = Bytes("To the east is the living room.")




computer = Bytes("""The screen shows the following:
\033[38;2;138;226;52m\033[48;2;0;21;0m
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




sign = Bytes("""
\033[38;5;2mSale!
Only 0.02 ALGO per item\033[0m

To buy an item (if using the 'avmloop' client), enter the following command:
\033[38;2;138;226;52m\033[48;2;0;21;0m
> /optin 23423423,/pay 0.02,buy junk\033[0m
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
    	If( l == Bytes('D'), Return( dining_connects )
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
    	Log(Concat(Bytes("Trying to move "),direction)),
    	While( i.load() < Len(connects.load())).Do(
          Seq(
    	     If( Extract(connects.load(), i.load(), Int(1)) == direction, 
                     Seq(
    	                App.localPut(Int(0),Bytes('location'), Extract(connects.load(), i.load() + Int(1), Int(1))),
    	                d.store(show(lgets(Bytes('location')))),
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
    	show_at_location_(),
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
    	If( l == Bytes('D'), printloc(dining, dining_conn_descr, dining_connects)
         ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def show_inventory_():
    i = ScratchVar(TealType.uint64)
    inv = StringArray(lgets(Bytes('inventory')))
    return  Seq(
    	Log(Bytes("You are carrying:")),
    	Log(fgYellow),
    	inv.init(),
    	i.store(Int(0)),
    	While( i.load() < inv.size.load()).Do(
          Seq(
    	     Log(abi.String(inv[i.load()]).value),
    	     i.store(i.load() + Int(1)) )
       ),
    	Log(resetColor),
    	Return( Int(1) ) )



@Subroutine(TealType.none)
def show_junk():    
  return Log(Concat(numtostr( asset_bal(Global.current_application_address(), Int(0))),Bytes(" Garage Sale Junk")))


@Subroutine(TealType.none)
def show_at_location_():
    i = ScratchVar(TealType.uint64)
    n = ScratchVar(TealType.uint64)
    items = StringArray(ggets(Concat(lgets(Bytes('location')),Bytes('_items'))))
    return  Seq(
    	items.init(),
    	If( items.size.load() == Int(0), 
          n.store(Int(0))
        , 
            Seq(
    	       Log(Bytes('You see the following items here:')),
    	       Log(fgPurple),
    	       i.store(Int(0)),
    	       While( i.load() < items.size.load()).Do(
                   Seq(
    	              Log(abi.String(items[i.load()]).value),
    	              i.store(i.load() + Int(1)) )
                ),
    	       If( lgets(Bytes('location')) == Bytes('D'), 
                     show_junk()
                  ) )
       ),
    	Log(resetColor) )



@Subroutine(TealType.none)
def printitem(i):
    return  Seq(
    	Log(fgWhite),
    	If( i == Bytes('computer'), Log(computer)
         ),
    	If( i == Bytes('note'), Log(note)
         ),
    	If( i == Bytes('sign'), Log(sign)
         ),
    	Log(resetColor) )



@Subroutine(uint64)
def exists_item(item, loc):
    return  Seq(
    	If( And( loc == Bytes('S'), (Or( item == Bytes('computer'), item == Bytes('books') )) ), 
          Return( Int(1) )
         ),
    	If( And( loc == Bytes('D'), item == Bytes('sign') ), 
          Return( Int(1) )
         ),
    	If( item == Bytes('note'), 
          Return( Int(1) )
         ),
    	Return( Int(0) ) )



@Subroutine(uint64)
def rolld20():
  return ( rnd(Int(1), Int(20)) )


@Subroutine(uint64)
def examine_(i):
    s = ScratchVar(TealType.bytes)
    return  Seq(
    	If( exists_item(i, lgets(Bytes('location'))),     
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
def encounter():
    return  Seq(
    	Log(Bytes('A')),
    	Log(Concat(fgRed, clr(Bytes('Bitcoin Maximalist '), bgWhite), fgRed, resetColor)),
    	Log(Bytes('suddenly appears. He attacks you with')),
    	Log(Concat(clr(Bytes('Nonsense'), fgRed), resetColor)),
    	Log(Bytes('and runs away.')),
    	Log(Concat(clr(Bytes('You lose [10] hit points'), bgRed), fgWhite, resetColor)),
    	Return( Int(1) ) )



@Subroutine(uint64)
def buy_(what):
    return  Seq(
    	Log(Bytes("You bought it.")),
    	Return( Int(1) ) )



@Subroutine(uint64)
def find_axfer(assetid):
    found = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    return  Seq(
    	i.store(Int(0)),
    	found.store(Int(0)),
    	While( i.load() < Global.group_size()).Do(
          Seq(
    	     If( (And( Gtxn[i.load()].asset_id == assetid, And( Gtxn[i.load()].asset_receiver() == Global.current_application_address(), Gtxn[i.load()].asset_amount() == Int(1) ) )), 
                   found.store(Int(1))
                  ),
    	     i.store(i.load() + Int(1)) )
       ),
    	Return( found.load() ) )



@Subroutine(uint64)
def offer_(asset, what):
    return  Seq(
    	If( what == Bytes("junk"), 
            Seq(
    	       InnerTxnBuilder.Begin(),
    	       InnerTxnBuilder.SetFields({
                 TxnField.type_enum: TxnType.AssetTransfer,
                 TxnField.sender: Global.current_application_address(),
                 TxnField.asset_amount: Int(0),
                 TxnField.asset_receiver: Global.current_application_address(),
                 TxnField.xfer_asset: Txn.assets[asset]
               }),
    	       InnerTxnBuilder.Submit(),
    	       Log(Bytes("The merchant will take your junk.")),
    	       Return( Int(1) ) )
       ),
    	Return( Int(0) ) )



@Subroutine(uint64)
def use_(item:bytes):
    roll = ScratchVar(TealType.uint64)
    return  Seq(
    	If( arr_find(lgets(Bytes('inventory')), item) == NOT_FOUND, 
            Seq(
    	       Log(Bytes('You are not carrying that.')),
    	       Return( Int(1) ) )
       ),
    	If( Or( item == Bytes('die'), Or( item == Bytes('dice'), item == Bytes('d20') ) ), 
            Seq(
    	       Log(Bytes("Rolling d20...")),
    	       Log(fgYellow),
    	       roll.store(Int(0)),
    	       roll.store(rolld20()),
    	       Log(Concat(Bytes("[ "),Concat(numtostr(roll.load()),Bytes(" ]")))),
    	       Log(resetColor),
    	       If( roll.load() < Int(10), 
                     Return( encounter() )
                  ) )
        , 
          Log(Bytes("You can't use that."))
         ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def take_(what:TealType.bytes):
    ind = ScratchVar(TealType.uint64)
    inv = StringArray(lgets(Bytes('inventory')))
    return  Seq(
    	ind.store(Int(0)),
    	ind.store(arr_find(ggets(Concat(lgets(Bytes('location')),Bytes('_items'))), what)),
    	If( ind.load() == NOT_FOUND, 
          Log(Bytes('You do not see that here, or it is not something you can take.'))
        , 
            Seq(
    	       inv.init(),
    	       inv.append(abi.String.encode(what)),
    	       App.localPut(Int(0),Bytes('inventory'), inv.serialize()),
    	       App.globalPut(Concat(lgets(Bytes('location')),Bytes('_items')), arr_del(ggets(Concat(lgets(Bytes('location')),Bytes('_items'))), ind.load())),
    	       Log(Concat(Bytes('You take the '),what)) )
       ),
    	Return( Int(1) ) )



@Subroutine(uint64)
def drop_(what:TealType.bytes):
    ind = ScratchVar(TealType.uint64)
    items = StringArray(ggets(Concat(lgets(Bytes('location')),Bytes('_items'))))
    return  Seq(
    	ind.store(Int(0)),
    	ind.store(arr_find(lgets(Bytes('inventory')), what)),
    	If( ind.load() == NOT_FOUND, 
          Log(Bytes('You are not carrying that.'))
        , 
            Seq(
    	       App.localPut(Int(0),Bytes('inventory'), arr_del(lgets(Bytes('inventory')), ind.load())),
    	       items.init(),
    	       items.append(abi.String.encode(what)),
    	       Log(Concat(Bytes('You dropped the '),what)),
    	       App.globalPut(Concat(lgets(Bytes('location')),Bytes('_items')), items.serialize()) )
       ),
    	Return( Int(1) ) )



@Subroutine(TealType.none)
def init_local_array(name):
    strarr = StringArray(Bytes(""))
    return  Seq(
    	strarr.init(),
    	If( name == Bytes('inventory'), 
          strarr.append(abi.String.encode(Bytes('note')))
         ),
    	App.localPut(Int(0),name, strarr.serialize()) )



@Subroutine(TealType.none)
def init_global_array(name):
    strarr = StringArray(Bytes(""))
    return  Seq(
    	strarr.init(),
    	If( name == Bytes('S_items'), 
          strarr.append(abi.String.encode(Bytes('d20')))
         ),
    	If( name == Bytes('D_items'), 
          strarr.append(abi.String.encode(Bytes('sign')))
         ),
    	App.globalPut(name, strarr.serialize()) )



@Subroutine(uint64)
def setup_():
    return  Seq(
    	App.localPut(Int(0),Bytes('location'), Bytes('Y')),
    	init_local_array(Bytes('inventory')),
    	init_global_array(Bytes('Y_items')),
    	init_global_array(Bytes('L_items')),
    	init_global_array(Bytes('S_items')),
    	init_global_array(Bytes('D_items')),
    	Return( Int(1) ) )



class ABIApp(DefaultApprove):

  @staticmethod
  @ABIMethod
  def look() -> abi.Uint32:
    return ( show(lgets(Bytes('location'))) )

  

  @staticmethod
  @ABIMethod
  def setup() -> abi.Uint32:
    return ( setup_() )

  

  @staticmethod
  @ABIMethod
  def move(dir: String) -> abi.Uint32:
    return ( move_(lgets(Bytes('location')), abi.String(dir).value) )

  

  @staticmethod
  @ABIMethod
  def take(what: String) -> abi.Uint32:
    return ( take_(abi.String(what).value) )

  

  @staticmethod
  @ABIMethod
  def drop(what: String) -> abi.Uint32:
    return ( drop_(abi.String(what).value) )

  

  @staticmethod
  @ABIMethod
  def inventory() -> StringArray:
    return ( lgets(Bytes('inventory')) )

  

  @staticmethod
  @ABIMethod
  def examine(what: String) -> abi.Uint32:
    return ( examine_(abi.String(what).value) )

  

  @staticmethod
  @ABIMethod
  def use(item: String) -> abi.Uint32:
    return ( use_(abi.String(item).value) )

  

  @staticmethod
  @ABIMethod
  def buy(item: String) -> abi.Uint32:
    return ( buy_(abi.String(item).value) )    

  

  @staticmethod
  @ABIMethod
  def offer(asset, item: String) -> abi.Uint32:
    return ( offer_(Int(0), abi.String(item).value) )    



if __name__ == "__main__":

  def find_method(methods, name):
    for m in methods:
      if m['name'] == name:
        return m['args']
  
  def addtxns(l, d):
    for x in l:
      xargs = l[x]
      for a in xargs:
        (mth, typ, ind) = a
        find_method(d, mth).insert(ind, {"type": typ}) 

  app = ABIApp()

  currint = {}
  try:
    currjson = open('abiadv.json').read()
    currint = json.loads(currjson)    
  except:
    pass
    
  currint['methods'] = app.get_interface().dictify()['methods']

  txnargs = json.loads('{"buy": [["buy", "axfer", 0], ["buy", "pay", 1]]}') 
  addtxns(txnargs, currint['methods'])

  #refargs = json.loads('{refargs}') 
  #addtxns(refargs, currint['methods'])
  
  with open("abiadv.json", "w") as f:
    f.write(json.dumps(currint, indent=4))

  print(compileTeal(app.handler(), mode=Mode.Application, version=5, assembleConstants=True))
  
