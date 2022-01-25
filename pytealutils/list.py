from pyteal import (
    Len,
    Concat,
    Extract,
    ExtractUint16,
    ExtractUint32,
    ExtractUint64,
    Substring,
    Itob,
)
from pyteal import TealType, Expr, Int, ScratchVar, Subroutine, Seq
from enum import Enum

# sort - In place? Spool to stack?
# reduce - (sum, mean, max, min)
# map - Same type only?
# Other list types? allow uvarints? dynamic length byte strings?


# Enum
uint16 = Int(16)
uint32 = Int(32)
uint64 = Int(64)


class List:
    _internal = ScratchVar()

    def __init__(self, size: Int):
        # TODO: Make sure its in the enum
        self.size = size
        self.byte_size = size / Int(8)

    def set(self, data: TealType.bytes) -> Expr:
        # TODO: Check that length is factor of size
        return self._internal.store(data)

    def get(self) -> TealType.bytes:
        return self._internal.load()

    def __getitem__(self, idx: TealType.uint64) -> Expr:
        # TODO: Make sure its not outside the list
        if self.size.value == 16:
            return ExtractUint16(self.get(), idx * self.byte_size)
        elif self.size.value == 32:
            return ExtractUint32(self.get(), idx * self.byte_size)
        else:
            return ExtractUint64(self.get(), idx * self.byte_size)

    def __setitem__(self, idx: TealType.uint64, value: TealType.uint64) -> Expr:
        return self.store(
            Concat(
                Substring(self.get(), Int(0), idx * self.byte_size),
                Itob(value),  # TODO: Take only the last `byte_size` byes?
                Substring(self.get(), idx * self.byte_size, Len(self.get())),
            )
        )

    def __delitem__(self, idx: TealType.uint64) -> Expr:
        return self.store(
            Concat(
                Substring(self.get(), Int(0), idx * self.byte_size),
                Substring(self.get(), (idx + Int(1)) * self.byte_size, Len(self.get())),
            )
        )

    def get_bytes(self, idx: TealType.uint64) -> Expr:
        return Substring(
            self.get(), idx * self.byte_size, (idx + Int(1)) * self.byte_size
        )

    def swap(self, idx1: TealType.uint64, idx2: TealType.uint64) -> Expr:
        # Store both in stack or state and write back
        elem1, elem2 = ScratchVar(), ScratchVar()
        return Seq(
            elem1.store(self.get_bytes(idx1)),
            elem2.store(self.get_bytes(idx2)),
            # Put bytes
            self.store(),
        )

    def __len__(self) -> TealType.uint64:
        return Len(self.get()) / self.byte_size
