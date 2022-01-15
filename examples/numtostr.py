@bytes
def numtostr(n):
  out = "             "
  i = 0
  while True:
    digit = n % 10
    out = SetByte(out, 2-i, digit+48)
    n = n / 10		
    if n == 0:
      return out
    i = i + 1

def app():
  print(numtostr(45))
