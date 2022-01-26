from lib.util import *

def proc(n):
  return n * 2

def acceptable(n, target):
  if n >= target:
    print("Acceptable. Diff is " + numtostr(n - target))
    return True
  else:
    return False

def app():
  total = 1
  i = 0
  while not acceptable(total, Btoi(Txn.application_args[0])):
    total = proc(total)
    i += 1
  return i
