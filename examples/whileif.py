def app():
  target = 100
  total = 1
  diff = 99999
  i = 0
  while total < target:
    total *= 2
    i += 1
    if total > target:
      diff = target - total
  return diff
