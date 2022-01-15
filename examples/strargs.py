def app():
  name = ""
  name = Txn.application_args[0]
  age = Btoi(Txn.application_args[1])
  if age > 65:
    Log("User " + name + " is at retirement age.")
    return 1
  else:
    Log("User " + name + " is still young.")
    return 0
