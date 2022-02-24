
import json
from typing import Tuple

from pyteal import *

from pytealutils.applications import ABIMethod, DefaultApprove
from pytealutils.applications.application import set_tx_args

from pytealutils import abi

globals().update(TealType.__members__)


from lib.util import *


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
    	If( lgeti(Bytes('junk_count')) > Int(0), 
          Log(Concat(numtostr(lgeti(Bytes('junk_count'))),Bytes(' Garage Sale Junk')))
         ),
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
def buy_(asset, what):
    asset_bal
    return  Seq(
    	If( find_payment(Int(20000)), 
            Seq(
    	       InnerTxnBuilder.Begin(),
    	       InnerTxnBuilder.SetFields({
                 TxnField.type_enum: TxnType.AssetTransfer,
                 TxnField.sender: Global.current_application_address(),
                 TxnField.asset_amount: Int(1),
                 TxnField.asset_receiver: Txn.sender(),
                 TxnField.xfer_asset: Txn.assets[Btoi(asset)]
               }),
    	       InnerTxnBuilder.Submit(),
    	       Log(Bytes("You bought it.")),
    	       App.localPut(Int(0),Bytes('junk_count'), asset_bal(Txn.sender(), Int(0))),
    	       Return( Int(1) ) )
       ),
    	Return( Int(0) ) )

@Subroutine(uint64)
def find_payment(amount):
    found = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    return  Seq(
    	i.store(Int(0)),
    	found.store(Int(0)),
    	While( i.load() < Global.group_size()).Do(
          Seq(
    	     If( (And( Gtxn[i.load()].sender() == Txn.sender(), And( Gtxn[i.load()].receiver() == Global.current_application_address(), Gtxn[i.load()].amount() == amount ) )), 
                   found.store(Int(1))
                  ),
    	     i.store(i.load() + Int(1)) )
       ),
    	Return( found.load() ) )

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
def init_global_array(name, df):
    strarr = StringArray(Bytes(""))
    return  Seq(
    	strarr.init(),
    	If( df != Bytes(''), 
          strarr.append(abi.String.encode(df))
         ),
    	App.globalPut(name, strarr.serialize()) )

@Subroutine(uint64)
def setup_():
    return  Seq(
    	App.localPut(Int(0),Bytes('location'), Bytes('Y')),
    	App.localPut(Int(0),Bytes('junk_count'), Int(0)),
    	init_local_array(Bytes('inventory')),
    	init_global_array(Bytes('Y_items'), Bytes('')),
    	init_global_array(Bytes('L_items'), Bytes('')),
    	init_global_array(Bytes('S_items'), Bytes('d20')),
    	init_global_array(Bytes('D_items'), Bytes('sign')),
    	Return( Int(1) ) )


set_tx_args({"buy": ["axfer", "pay"]})

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
  def buy(asset, item: String ) -> abi.Uint32:
    return ( buy_(asset, abi.String(item).value) )    


  
  @staticmethod
  @ABIMethod
  def offer(asset, item: String) -> abi.Uint32:
    return ( offer_(asset, abi.String(item).value) )    





  
if __name__ == "__main__":

  app = ABIApp()

  currint = {}
  try:
    currjson = open('abiadv.json').read()
    currint = json.loads(currjson)    
  except:
    pass
    
  currint['methods'] = app.get_interface().dictify()['methods']
    
  with open("abiadv.json", "w") as f:
    f.write(json.dumps(currint, indent=4))

  print(compileTeal(app.handler(), mode=Mode.Application, version=5, assembleConstants=True))
  
