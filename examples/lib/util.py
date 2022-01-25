from typing import Tuple
from pytealutils.abi import ABIDynamicArray

class StringArray(ABIDynamicArray[Tuple[String]]):
    pass

def arr_del(str_arr, to_remove):
  new_arr = StringArray()
  i = 0
  while i < to_remove:
    newlist.append(str_arr[i])
    i = i + 1
  i = i + 1
  while i < str_arr.size.load():
    newlist.append(str_arr[i])
    i = i + 1
  return new_arr

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
