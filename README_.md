# genpyteal

Converts Python to PyTeal. Your mileage will vary depending on how much you deviate from the examples.
Its quite easy to get an error by doing something not supported.  However, it often still outputs useful PyTeal that you can then
fix up.

If you appreciate this tool, you are welcome to send ALGOs to `RMONE54GR6CYOJREKZQNFCZAUGJHSPBUJNFRBTXS4NKNQL3NJQIHVCS53M`.
## Installation

`pip3 install genpyteal` or `pip install genpyteal`

### ABI 


As of this writing, if you use any ABI stuff, you will need to uninstall regular pyteal and do this:
`pip install -e git+https://github.com/algorand/pyteal@abi-types#egg=pyteal`

`b67a71a224eb1b8c477ae32b5c4d0ab01a680edb`

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

