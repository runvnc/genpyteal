from ast import *
from typing import Any


class RewriteConsts(NodeTransformer):
    def visit_Constant(self, node: Constant) -> Any:
        t = type(node.value)
        if t is int:
            return self.wrapInt(node.value)
        elif t in [bytes, str]:
            return self.wrapBytes(node.value)
        else:
            return node

    def wrapInt(self, value: int) -> Call:
        return Call(
            func=Name(id="Int", ctx=Load()),
            args=[Constant(value=value)],
        )

    def wrapBytes(self, value) -> Call:
        return Call(
            func=Name(id="Bytes", ctx=Load()),
            args=[Constant(value=value)],
        )
