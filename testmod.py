import json
from redbaron import RedBaron

def catchdump(x):
  try:    
    return x.dumps()      
  except:
    pass  

def convertAll(red):
  ifs = red.find_all('ifelseblock')
  ifs.map(lambda x: convertIfs(x))
  strs_ = []
  cnt = 0  
  for nd in red:
    cnt += 1
    nodes = nd.find_all(['ifelseblock','atomtrailers'], recursive=False)
    strs = nodes.map(catchdump)
    strs = strs.filter(lambda x: x != None)
    strs_.extend(strs)
  if len(strs_) > 1:
    red.value = 'Seq([' + ',\n'.join(strs_) + '])\n'

def convertIfs(if_):
  convertAll(if_.value)
  if_.value = 'If(' + if_.value[0].test.dumps() + ', ' + if_.value[0].value.dumps() +')\n\n'

def convert(fname):
  source = open(fname, "r")
  red = RedBaron(source.read())  
  print(red.dumps())
  print('---------------------------------------------')
  print()
  fundefs = red.find_all('def')
  fundefs.map(lambda x: convertAll(x))
  print(red.dumps())

convert('iftest.py')
