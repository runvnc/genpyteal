target = 100

def proc(n):
  return n * 2

def acceptable(n):
  if n >= target:
    print("Acceptable. Diff is:")
    print(n - diff)
    return True
  else:
    return False

def app():
  total = 1
  i = 0
  while not acceptable(total):
    total = proc(total)
    i += 1
  return i
