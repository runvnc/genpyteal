#!/bin/env python3

import sys, json
from algosdk import abi
from contextlib import redirect_stdout

"""
def reverse(a: String) -> String:
  return reverse_(a)

def echo_first(a: StringArray) -> String:
  return a[0]

def add(a: Uint32, b: Uint32) -> Uint32:
  return a + b
"""

def fixtype(nm):
  return "{}".format(nm).title()


with open(sys.argv[1]) as f:
  str_ = f.read()  
  with open(sys.argv[2], 'w') as w:
    with redirect_stdout(w):
      #data = json.loads(f.read())
      interface = abi.Interface.from_json(str_)
      for f in interface.methods:
        defname = f.name
        args = ", ".join(map(lambda x: f"{x.name}: {fixtype(x.type)}", f.args))
        print(f"def {defname}({args}) -> {fixtype(f.returns)}:\n")
        print()

      print('def delete():\n')
      print()
