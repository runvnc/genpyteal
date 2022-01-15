def proc(n):
  return n * 2

def acceptable(n, target):
  if n >= target:
    print("Acceptable. Diff is:")
    print(Itob(n - target))
    return 1
  else:
    return 0

def app():
  total = 1
  i = 0
  while not acceptable(total, Btoi(Txn.application_args[0])):
    total = proc(total)
    i += 1
  return i
