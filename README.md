# aoc2019
My solutions to Advent of Code 2019

## Day 1: python

## Day 2: python

## Day 3: C

## Day 4: python

## Day 5: python

## Day 6: python

## Day 7: python

## Day 8: python

## Day 9: python
After messing for an hour getting day 9 right, I decided on
another rewrite of the intcode emulator. The obvious source of confusion was the
handling of operands and their modes for every single opcode. Now they are
handled once, by one function, before being passed on. This makes separate
function calls unnecessary; they are replaced by a switch like construct of
`if/elif/else`. Note that operands are now separated into read/write. Thanks to
/u/1vader for the idea of the dictionary `self.opcodes`.

Code for both parts resides in rewrite.py.

As a bonus a rudimentary assembler written in *flex/Bison* is included.

