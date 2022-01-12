sum = 1

def put(n,m):
  print(n,m)

def foo(b):
  put(sum, b)  

def fn1(n):
  foo(n+2)
  foo(n-2)

def test(x):
  if x == 1:
    fn1()
