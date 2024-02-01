StackPush = "sp"  # int
StackDrop = "sd"
StackDup = "sc"

DumpInteger = "di"
DumpCharacter = "dc"
DumpStr = "ds"

CallAddr = "ca"
CallReturn = "cr"

JmpIf = "ji"
JmpAlways = "ja"

MathAdd = "ma"
MathSub = "ms"
MathMul = "mm"
MathDiv = "md"

AllocStr = "as"  # str

Halt = "h"

OP = {
    "s": {"p": StackPush, "d": StackDrop, "c": StackDup},
    "d": {"i": DumpInteger, "c": DumpCharacter, "s": DumpStr},
    "c": {"a": CallAddr, "r": CallReturn},
    "j": {"i": JmpIf, "a": JmpAlways},
    "m": {"a": MathAdd, "b": MathSub, "m": MathMul, "d": MathDiv},
    "a": {"s": AllocStr},
    "h": Halt,
}
