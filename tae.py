import tal
import sys
import time


class Memory:
    def __init__(self) -> None:
        self._mem: bytearray = bytearray()

    def write(self, data: bytes) -> int:
        ptr = len(self._mem)
        for ii in data:
            self._mem.append(ii)
        return ptr

    def read(self, ptr: int, sz: int) -> bytes:
        return self._mem[ptr : (ptr + sz)]


class Ctx:
    def __init__(self) -> None:
        self.mem = Memory()
        self.stack = []
        self.callstack = []
        self.loopstack = []
        self.code = []
        self.ip = 0

    def stackpush(self, num: int):
        self.code.append(lambda: self.stack.append(num))

    def stackdrop(self):
        self.code.append(lambda: self.stack.pop())

    def stackdup(self):
        self.code.append(lambda: self.__dup())

    def dumpinteger(self):
        self.code.append(lambda: print(self.stack.pop()))

    def dumpcharacter(self):
        self.code.append(lambda: self.__stdout_c(self.stack.pop()))

    def dumpstr(self):
        self.code.append(lambda: self.__stdout_s(self.stack.pop()))

    def calladdr(self):
        self.code.append(lambda: self.__call(self.stack.pop()))

    def callreturn(self):
        self.code.append(lambda: self.__ret())

    def jmpif(self):
        self.code.append(lambda: self.__jmpif())

    def jmpalways(self):
        self.code.append(lambda: self.__jmp())

    def mathadd(self):
        self.code.append(lambda: self.stack.append(self.stack.pop() + self.stack.pop()))

    def mathsub(self):
        self.code.append(lambda: self.stack.append(self.stack.pop() - self.stack.pop()))

    def mathmul(self):
        self.code.append(lambda: self.stack.append(self.stack.pop() * self.stack.pop()))

    def mathdiv(self):
        self.code.append(lambda: self.stack.append(self.stack.pop() / self.stack.pop()))

    def allocstr(self, s: str):
        self.code.append(lambda: self.stack.append(self.mem.write(s.encode() + b"\0")))

    def halt(self):
        self.code.append(lambda: self.__hlt())

    def __stdout_s(self, s: int):
        _s = b""
        while (b := self.mem.read(s, 1)) != b"\0":
            s += 1
            _s += b
        print(_s.decode(), end="")

    def __stdout_c(self, c: int):
        sys.stdout.write(c.to_bytes((c.bit_length() + 7) // 8, "little").decode())

    def __jmpif(self):
        addr = self.stack.pop()
        cond = self.stack.pop()
        # print(f"if {cond} jmp {addr}")
        if cond > 0:
            self.ip = addr

    def __jmp(self):
        addr = self.stack.pop()
        # print(f"jmp {addr}")
        self.ip = addr

    def __dup(self):
        a = self.stack.pop()
        self.stack.append(a)
        self.stack.append(a)

    def __call(self, addr: int):
        self.callstack.append(self.ip)
        self.ip = addr

    def __ret(self):
        self.ip = self.callstack.pop()

    def __hlt(self):
        self.ip = -1

    def __call__(self):
        self.stack = []
        self.ip = 0
        while self.ip < len(self.code) and self.ip >= 0:
            op = self.code[self.ip]
            self.ip += 1
            op()
            # print("at", self.ip, self.stack)


class Program:
    def __init__(self, src: str) -> None:
        self.src = src
        self.index = 0
        self.ip = 0
        self.checkpoints = {}
        self.ctx = Ctx()
        self.instr = False

    def n(self) -> str:
        self.index += 1
        if not self.instr:
            while self.index < len(self.src) and self.src[self.index - 1] in "\n\t ":
                self.index += 1
        return self.src[self.index - 1]

    def p(self) -> str:
        if not self.instr:
            while self.index < len(self.src) and self.src[self.index] in "\n\t ":
                self.index += 1
        return self.src[self.index]

    def pint(self) -> int:
        n = 0
        mul = 1
        if self.p() == "-":
            mul = -1
            self.n()
        while self.index < len(self.src) and self.p().isdigit():
            n = n * 10 + int(self.n())
        return n * mul

    def pstr(self) -> str:
        self.instr = True
        s = ""
        escaping = False
        while True:
            c = self.n()
            if escaping:
                match c:
                    case "\\":
                        s += "\\"
                    case "n":
                        s += "\n"
                    case "t":
                        s += "\t"
                    case "r":
                        s += "\r"
                    case _:
                        raise Exception(f"unescapable character: {c}")
                escaping = False
            elif c == "\\":
                escaping = True
            elif c in "'\"":
                self.instr
                return s
            else:
                s += c

    def paddr(self) -> int:
        isref = False
        iscur = False
        if self.p() == "@":
            self.n()
            isref = True
        elif self.p() == ".":
            self.n()
            iscur = True
        cpid = self.pint()
        if isref:
            return self.checkpoints[cpid]
        elif iscur:
            return self.ip + cpid
        return cpid

    def gop(self, op: str):
        match op:
            case tal.StackPush:
                self.ctx.stackpush(self.paddr())
            case tal.StackDrop:
                self.ctx.stackdrop()
            case tal.StackDup:
                self.ctx.stackdup()
            case tal.DumpInteger:
                self.ctx.dumpinteger()
            case tal.DumpCharacter:
                self.ctx.dumpcharacter()
            case tal.DumpStr:
                self.ctx.dumpstr()
            case tal.CallAddr:
                self.ctx.calladdr()
            case tal.CallReturn:
                self.ctx.callreturn()
            case tal.JmpIf:
                self.ctx.jmpif()
            case tal.JmpAlways:
                self.ctx.jmpalways()
            case tal.MathAdd:
                self.ctx.mathadd()
            case tal.MathSub:
                self.ctx.mathsub()
            case tal.MathMul:
                self.ctx.mathmul()
            case tal.MathDiv:
                self.ctx.mathdiv()
            case tal.AllocStr:
                self.ctx.allocstr(self.pstr())
            case tal.Halt:
                self.ctx.halt()
            case _:
                raise Exception("unsupported instruction")
        self.ip += 1

    def cop(self, from_: dict[str, str | dict], prev: str = ""):
        c = self.n()
        if c in "\n\t ":
            return
        if c not in from_.keys():
            raise Exception(f"unknown op: {prev}{c}")

        completepath = prev + c
        v = from_[c]
        if isinstance(v, str):
            self.gop(completepath)
        elif isinstance(v, dict):
            self.cop(v, completepath)

    def compile(self) -> Ctx:
        start = time.perf_counter()
        self.ctx = Ctx()
        while self.index < len(self.src):
            if self.p() == "#":
                self.n()
                self.checkpoints[(cpid := self.pint())] = self.ip
                print(f"new checkpoint #{cpid} -> {self.ip}")
            else:
                self.cop(tal.OP, "")
        self.time = time.perf_counter() - start
        return self.ctx


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no input file provided.")
        exit(1)
    file = sys.argv[1]

    with open(file) as f:
        src = f.read()

    script = Program(src)
    prog = script.compile()
    print(f"compiled in {script.time}s")
    start = time.perf_counter()
    prog()
    run_time = time.perf_counter() - start
    print(f"ran in {run_time}s")
