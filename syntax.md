# Syntax

Spaces, newlines and tabs are ignored. Comments are not supported

## Basic instructions

Push an integer to the stack with `sp65`. `sp` means `stack.push`. The integer
is inserted directly after the op. Other ops in the stack namespace are:

- _drop_ (`sd`): drop one element from the stack.

Numbers can also be dumped to the terminal. For dumping to the terminal the
_dump_ (`d`) namespace is used. These are all the supported _dump_ ops:

- _integer_ (`di`) prints an integer from the stack to the terminal.
- _character_ (`dc`) prints an integer from the stack to the terminal as a
character.

## Operands

Operands are used for example with the `sp` instruction. An integer can be
negative. To note addresses, an integer can be prefixed with `.` to indicate
an offset from the current address. Some examples: `.3`, `.-9`.

Addresses can also be noted as checkpoints.

```tc
#0
sp@0
```

In the above example, the address of the checkpoint 0 is pushed to the stack.
Checkpoints can be defined with `#<num>`. If it already exists, it will be
overridden. The checkpoint can be referenced with `@<num>`. Checkpoints can be
negative.
