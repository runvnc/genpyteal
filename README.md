# genpyteal

Converts Python to PyTeal. Your mileage will vary depending on how much you deviate from the examples.
Its quite easy to get an error by doing something not supported.  However, it often still outputs useful PyTeal that you can then
fix up.


## Installation

`pip3 install genpyteal` or `pip install genpyteal`

*Warning*: The scripts have `python3` in them because that is what works on my system. It only works with Python 3. 
There might be some system where it needs to say `python` instead.  If so, maybe just pull the code from the github repo to change it?

## Usage

To generate PyTeal:

`genpyteal thescript.py`

To generate PyTeal and do syntax highlighting (requires `pygmentize` and `boxes` to be installed):

`genpyteal thescript.py | niceout`

To generate PyTeal and then TEAL:

`genteal thescript.py`

To show the AST (FST) of a Python program (uses RedBaron .help(), and requires `ipython` installed):

`showast thescript.py`

## Supported constructs

`statement list` (= Seq), `integer const` ( = Int(n)), `if/else`, `while`, `print` (= `Log`), `+` ( = Concat(str1, str2) ), 
`True/False` (= 1/0), `and/or/not` ...
(maybe something I am forgetting).

## Details

You can use a subset of Python. For scratch variables, you will need to initialize them at the beginning of a function, such as `x = 0` or `s = "tom"`. It uses 
that to determine the type. Sometimes you may need to specify Bytes or Int still. Integer/string literals get Int/Bytes added automatically. You can use `print` instead of Log. 

Name the main function `app` to indicate a stateful application contract, or `sig` for a LogicSig contract.

For transaction fields, you can leave off the parenthesis, e.g. `Txn.sender` instead of `Txn.sender()`.

It will assume functions return `uint64` unless you specify `@bytes` or there is no return, which will automatically insert `@Subroutine(TealType.none)`

If you want to print a number in the log, you can use the numtostr function I made:

```python
from lib import util

def app():
  print("Your number is " + util.numtostr(100))

```

The best explanation is just to show the examples.

## Examples

## examples/bool.py 

```python
def app():
  amt = 15
  return amt > 10 and amt < 20 or amt == 0
```
## examples/callscratch.py 

```python
def g(x):
    return 3

def f(n):
    return g(n)

def app():
    x = f(30)
    name = "Bob"
    print(name)
    return 100
```
## examples/checkgroup.py 

```python
PAYTO = Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY')
FEE = 10 * 1000000
ZERO = Global.zero_address()

def no_close_to(i):
  Assert( Gtxn[i].close_remainder_to == ZERO )

def no_rekey(i):
  Assert( Gtxn[i].rekey_to == ZERO )

def verify_payment(i):
  Assert( Gtxn[i].receiver == PAYTO and
          Gtxn[i].amount == Int(FEE) and
          Gtxn[i].type_enum == TxnType.Payment )
         
def app():
  Assert( Global.group_size == 2 )
  
  no_close_to(1)
  no_rekey(1)

  verify_payment(1)

  App.globalPut('lastPaymentFrom', Gtxn[1].sender)
  Approve()
```
## examples/ifseq.py 

```python

def foo(b):
  x = b

def app():
  foo(10)
  if 1 == 1:
    return 1
  else:
    return 0
```
## examples/inner.py 

```python

def pay(amount: uint64, receiver: bytes):
    Begin()
    SetFields({
        TxnField.type_enum: TxnType.Payment,
        TxnField.sender: Global.current_application_address,
        TxnField.amount: amount,
        TxnField.receiver: receiver
        })
    Submit()

def app():
    pay(10, Addr('6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY'))
    result = 0
    if Txn.first_valid > 1000000:
        result = 1
    return result

```
## examples/strargs.py 

```python
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
```
## examples/swap.py 

```python
"""Atomic Swap"""

alice = Addr("6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY")
bob = Addr("7Z5PWO2C6LFNQFGHWKSK5H47IQP5OJW2M3HA2QPXTY3WTNP5NU2MHBW27M")
secret = Bytes("base32", "2323232323232323")
timeout = 3000
ZERO_ADDR = Global.zero_address()

def sig(
    tmpl_seller=alice,
    tmpl_buyer=bob,
    tmpl_fee=1000,
    tmpl_secret=secret,
    tmpl_hash_fn=Sha256,
    tmpl_timeout=timeout,
):
    fee_cond = Txn.fee < Int(tmpl_fee)
    is_payment = Txn.type_enum == TxnType.Payment
    no_closeto = Txn.close_remainder_to == ZERO_ADDR
    no_rekeyto = Txn.rekey_to == ZERO_ADDR
    safety_cond = is_payment and no_rekeyto and no_closeto
    
    recv_cond = (Txn.receiver == tmpl_seller) and (tmpl_hash_fn(Arg(0)) == tmpl_secret)
    esc_cond = (Txn.receiver == tmpl_buyer) and (Txn.first_valid > Int(tmpl_timeout))

    return (fee_cond and safety_cond) and (recv_cond or esc_cond)
```
## examples/usenumtostr.py 

```python
from lib import util

def app():
  print("The best number is " + util.numtostr(42))
  return True
```
## examples/whilecallif.py 

```python
from lib import util

def proc(n):
  return n * 2

def acceptable(n, target):
  if n >= target:
    print("Acceptable. Diff is " + util.numtostr(n - target))
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
```
## examples/whilesum.py 

```python
def app():  
  totalFees = 0
  i = 0
  while i < Global.group_size:
    totalFees = totalFees + Gtxn[i].fee
    i = i + 1
  return 1
```

## lib/util.py
```python
@bytes
def numtostr(num):
  out = "             "
  i = 0
  digit = 0
  n = num
  done = False
  while not done:
    digit = n % 10
    out = SetByte(out, 12-i, digit+48)
    n = n / 10		
    if n == 0: done = True
    i = i + 1
  return Extract(out, 12 - i + 1, i)
```
