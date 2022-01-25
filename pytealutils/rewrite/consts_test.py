import ast
from consts import RewriteConsts

src = """
def f():
    x = 5
    x *= 10 

    y = "abc123"
    z = b"abc123"

    l = [1,2,3]
    n = l[4]

"""
tree = ast.parse(src)
RewriteConsts().visit(tree)
print(ast.dump(tree, indent=4))
