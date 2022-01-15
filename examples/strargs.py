def app():
  name = ""
  name = Txn.application_args[0]
  age = Btoi(Txn.application_args[1])
  if age > 65:
    print("User " + name + " is at retirement age.")
    return 1
  else:
    print("User " + name + " is still young.")
    return 0
