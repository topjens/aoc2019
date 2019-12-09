#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 08:01:33 2019

@author: jens
"""

with open("./input") as file:
    program = file.readline()
    
program = program.split(',')
program = list(map(int, program))
original_program = program.copy()

pc = 0
halt = False
input_stack = []

def reset_program():
    global program
    global halt
    global pc
    program = original_program.copy()
    halt = False
    pc = 0
    
def permutate(lst):
    # if lst is empty, return an empty list
    if len(lst) == 0:
        return []

    # if lst contains only one element, return it
    if len(lst) == 1:
        return [lst]
    
    l = []
    
    for i in range(len(lst)):
        m = lst[i]
        
        remain = lst[:i] + lst[i+1:]
        
        for p in permutate(remain):
            l.append([m] + p)
    return l
    

def do_add(par1, par2, par3, par1_mode, par2_mode):
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    program[par3] = par1 + par2
    return

def do_mult(par1, par2, par3, par1_mode, par2_mode):
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    program[par3] = par1 * par2
    return

def do_input(par1):
    #program[par1] = int(input())
    #program[par1] = int(input())
    program[par1] = int(input_stack.pop())
    return

def do_output(par1, par1_mode):
#    if(par1_mode == 0):
#        print(program[par1])
#    if(par1_mode == 1):
#        print(par1)
    if(par1_mode == 0):
        input_stack.append(program[par1])
    elif(par1_mode == 1):
        input_stack.append(par1)
    return

def do_jump_if_true(par1, par2, par1_mode, par2_mode):
    global pc
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    if(par1 != 0):
        pc = par2
    else:
        pc = pc + 3
    return

def do_jump_if_false(par1, par2, par1_mode, par2_mode):
    global pc
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    if(par1 == 0):
        pc = par2
    else:
        pc = pc + 3
    return

def do_less_than(par1, par2, par3, par1_mode, par2_mode):
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    if(par1 < par2):
        program[par3] = 1
    else:
        program[par3] = 0
    return

def do_equals(par1, par2, par3, par1_mode, par2_mode):
    if(par1_mode == 0):
        par1 = program[par1]
    if(par2_mode == 0):
        par2 = program[par2]
    if(par1 == par2):
        program[par3] = 1
    else:
        program[par3] = 0
    return

def do_instruction():
    global pc
    global halt
    opcode = program[pc]
    
    opcode = [int(i) for i in str(opcode)]
    
    while(len(opcode) != 5):
        opcode.insert(0, 0)
        
    par1_mode = opcode[2]
    par2_mode = opcode[1]
    par3_mode = opcode[0]
    opcode = opcode[3]*10+opcode[4]
    
    #print(program)
    
    if(opcode == 1):
        do_add(program[pc+1], program[pc+2], program[pc+3], par1_mode, par2_mode)
        pc = pc + 4
        return
    if(opcode == 2):
        do_mult(program[pc+1], program[pc+2], program[pc+3], par1_mode, par2_mode)
        pc = pc + 4
        return
    if(opcode == 3):
        do_input(program[pc+1])
        pc = pc + 2
        return
    if(opcode == 4):
        do_output(program[pc+1], par1_mode)
        pc = pc + 2
        return
    if(opcode == 5):
        do_jump_if_true(program[pc+1], program[pc+2], par1_mode, par2_mode)
        return
    if(opcode == 6):
        do_jump_if_false(program[pc+1], program[pc+2], par1_mode, par2_mode)
        return
    if(opcode == 7):
        do_less_than(program[pc+1], program[pc+2], program[pc+3], par1_mode, par2_mode)
        pc = pc + 4
        return
    if(opcode == 8):
        do_equals(program[pc+1], program[pc+2], program[pc+3], par1_mode, par2_mode)
        pc = pc + 4
        return
    if(opcode == 99):
        #print("HALT: End of execution")
        halt = True
        return
    print("Opcode %i not defined!" % opcode)
   
#while(halt != True):
#    do_instruction()

solutions = {}

for i in permutate(list('01234')):
    input_stack.append(0)
    for j in i:
        input_stack.append(j)
        reset_program()
        while(halt != True):
            do_instruction()
    solutions[input_stack.pop()] = i
    
for key in sorted(solutions.keys()):
    print("%s, %s" % (key, solutions[key]))
        
        