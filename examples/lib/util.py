from typing import Tuple

from pyteal import *

from pytealutils import abi

from .libex import *

StringArray = abi.DynamicArray[abi.String]

NOT_FOUND = Int(999)

@bytes
def clr(s, ansi):
  return Concat(ansi, s)

def arr_find(str_arr_bytes:bytes, item:bytes):
  str_arr = StringArray(str_arr_bytes)
  str_arr.init()
  i = 0
  while i < str_arr.size.load():
    if str_arr[i] == abi.String.encode(item):
      return i
    i = i +1
  return NOT_FOUND

@bytes
def arr_del(str_arr_bytes, index_to_remove):
  str_arr = StringArray(str_arr_bytes)
  new_arr = StringArray("")
  new_arr.init()
  str_arr.init()
  i = 0
  while i < index_to_remove:
    new_arr.append(str_arr[i])
    i = i + 1
  i = i + 1
  while i < str_arr.size.load():
    new_arr.append(str_arr[i])
    i = i + 1
  return new_arr.serialize()

def rnd(min_, max_):
  hash_ = ""
  rndcnt = 0
  rndcnt = App.globalGet('rndcnt')
  hash_ = Sha256(Concat(Txn.tx_id, Itob(Global.latest_timestamp)))  
  bigRand = Btoi(Extract(hash_ ,rndcnt, 7)) + Global.latest_timestamp % 100000
  rndcnt = rndcnt + 1
  App.globalPut('rndcnt', rndcnt)
  return min_ + bigRand % (max_ - min_ + 1)

@bytes
def numtostr(num):
  out = "             "
  i = 0
  digit = 0
  n = num
  done = False
  while not done:
    digit = n % 10
    out = SetByte(out, 12-i, digit+48)
    n = n / 10		
    if n == 0: done = True
    i = i + 1
  return Extract(out, 12 - i + Int(1), i)


