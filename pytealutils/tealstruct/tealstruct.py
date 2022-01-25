from pyteal import *
from typing import Tuple, Dict
from dataclasses import dataclass


@dataclass
class TealStruct:
    _data: ScratchVar = ScratchVar(TealType.bytes)
    # _conds: List[Tuple[Subroutine, Subroutine]]

    def __post_init__(self):
        pos = 0
        for k, v in self.__dataclass_fields__.items():
            if k == "_data":
                continue

            if hasattr(v.type, "__metadata__"):
                length = v.type.__metadata__[0]

            if v.type == "Int":
                length = 8

            self.__setattr__(k, self._getbytesimpl(pos, length))

            pos += length

    def init(self) -> Expr:
        @Subroutine(TealType.none)
        def _impl(data) -> Expr:
            return self._data.store(data)

        return _impl

    def _getbytesimpl(self, start, length) -> Expr:
        @Subroutine(TealType.bytes)
        def _impl():
            return Extract(self._data.load(), start, length)

        return _impl

    def _getintimpl(self, startvar) -> Expr:
        @Subroutine(TealType.uint64)
        def _impl():
            return ExtractUint64(self._data.load(), startvar)

        return _impl


# for field in definition:
#    self._conds.append([
#        matches(Bytes(field[0])),
#        [Int(pos), Int(field[1]), Int(field[2])]
#    ])
#    pos += field[1]

#
#

# def matches(fname):
#    @Subroutine(TealType.uint64)
#    def _impl(fcheck: TealType.bytes):
#        return fcheck == fname
#    return _impl
