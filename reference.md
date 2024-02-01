# Instruction reference

This is the documentation for all instructions. they will be noted as
`<num> op(num) <num>` for example. The argument types before the instruction
are expected on the stack. the ones after, are the result. The types inside the
parenthesis are operands in the code, like `sp 1`

## Stack

These instructions are prefixed with a `s`.

### Push: `sp(num) <num>`

Pushes the given integer to the stack.

### Drop: `<num> sd`

Drops a value from the stack.

### Duplicate: `<num> sc`

Duplicates a value from the stack.

## Dump

These instructions are prefixed with `d`.

### Integer: `<num> di`

Dumps an integer to the terminal.

### Character: `<num> dc`

Dumps an integer to the terminal as a byte, resulting in characters.

### String: `<num> ds`

Dumps a null-terminated string, read from the given pointer, to the terminal.

## Call

These instructions are prefixed with `c`.

### Call: `<addr> ca`

Jump to the specified address, storing the IP of origin in the call stack.

### Return: `cr`

Return to the address pushed by `ca`.

## Jump

These instructions are prefixed with `j`.

### If: `<condition> <addr> ji`

If `<condition>` is bigger than 0, jumps to `<addr>`.

### Always: `<add> ja`

Unconditional jump to `<addr>`.

## Math

These instructions are prefixed with `m`.

### Add: `<n2> <n1> ma <n>`

Adds `<n1>` + `<n2>`, and pushes the result.

### Subtract: `<n2> <n1> ma <n>`

Subtracts `<n1>` - `<n2>`, and pushes the result.

### Multiplies: `<n2> <n1> mm <n>`

Multiplies `<n1>` * `<n2>`, and pushes the result.

### Divide: `<n2> <n1> md <n>`

Divides `<n1>` / `<n2>`, and pushes the result.

## Allocate

These instructions are prefixed with `a`.

### String: `as(str) <num>`

Allocates a null-terminated string in memory, and pushes the pointer.

## Halt: `h`

Stops execution.
