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

## Day 10: python
**Needs to be cleaned up!**

## Day 11: python
On the surface easy modification of day 9. Write a small class
to deal with the robot, storing all the visited spaces with their `(x,y)` and
`color` in a `dict`. The IN opcode is rewritten to read from a function of the
robot class that gives the `color` at the current `(x,y)`, which takes its
arguments from a stack, the OUT opcode is rewritten to push its output to the
stack stack in stead of `stdout`.

Movement is done in the during the IN instruction, before IN is executed (I
first did this after, which let to unexpected output that took a while to
debug).

Part 2 reuses part of the code of day 8 to generate a pbm image. The image is
upside down because coordinates are given from top left, while we use cartesian
coordinates, but a call to imagemagick `convert -flip part2.pbm part2.png` fixes
this fast.