#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:25:06 2019

@author: jens
"""

stack = [0]

class intcode:   
    def __init__(self, program):
        with open(program) as file:
            self.memory = file.readline()

        self.memory = self.memory.split(',')
        self.memory = list(map(int, self.memory))
        self.original_memory = self.memory.copy()

        self.pc = 0
        self.halt = False
        self.done = False

        self.par1_mode = 0
        self.par2_mode = 0
        self.par3_mode = 0
        
        self.opcodes = dict([
            (1, self.do_add),
            (2, self.do_mult),
            (3, self.do_input),
            (4, self.do_output),
            (5, self.do_jump_if_true),
            (6, self.do_jump_if_false),
            (7, self.do_less_than),
            (8, self.do_equals),
            (99, self.do_halt),
        ])
        
        self.opcode_size = dict([
            (1, 4),
            (2, 4),
            (3, 2),
            (4, 2),
            (5, 0),
            (6, 0),
            (7, 4),
            (8, 4),
            (99, 0),
        ])

    def reset_program(self):
        self.memory = self.original_memory.copy()
        self.pc = 0
        self.halt = False
        self.done = False

    def do_add(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]
        par3 = self.memory[self.pc+3]
        
        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]
        
        self.memory[par3] = par1 + par2

    def do_mult(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]
        par3 = self.memory[self.pc+3]
        
        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]
        
        self.memory[par3] = par1 * par2

    def do_input(self):
        global stack
        par1 = self.memory[self.pc+1]
        self.memory[par1] = int(stack.pop())

    def do_output(self):
        global stack
        par1 = self.memory[self.pc+1]
        if(self.par1_mode == 0):
            par1 = self.memory[par1]

        stack.append(par1)
        self.halt = True
        

    def do_jump_if_true(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]

        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]

        if(par1 != 0):
            self.pc = par2
        else:
            self.pc += 3

    def do_jump_if_false(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]

        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]

        if(par1 == 0):
            self.pc = par2
        else:
            self.pc += 3

    def do_less_than(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]
        par3 = self.memory[self.pc+3]
        
        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]
        
        if(par1 < par2):
            self.memory[par3] = 1
        else:
            self.memory[par3] = 0

    def do_equals(self):
        par1 = self.memory[self.pc+1]
        par2 = self.memory[self.pc+2]
        par3 = self.memory[self.pc+3]
        
        if(self.par1_mode == 0):
            par1 = self.memory[par1]
        if(self.par2_mode == 0):
            par2 = self.memory[par2]
        
        if(par1 == par2):
            self.memory[par3] = 1
        else:
            self.memory[par3] = 0
            
    def do_int(self):
        print("INT")
        self.halt = False

    def do_halt(self):
        print("HALT")
        self.halt = True
        self.done = True

    def untangle_instruction(self, instruction):
        instruction = [int(i) for i in str(instruction)]
        
        while(len(instruction) != 5):
            instruction.insert(0, 0)
            
        self.par1_mode = instruction[2]
        self.par2_mode = instruction[1]
        self.par3_mode = instruction[0]

        return instruction[3]*10+instruction[4]

    def execute(self):
        self.halt = False
        while(self.halt == False):
            instruction = self.memory[self.pc]
            instruction = self.untangle_instruction(instruction)
            self.opcodes[instruction]()
            self.pc += self.opcode_size[instruction]
        return self.done

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

if __name__ == '__main__':
    solutions = {}
    pc1 = intcode('./input')
    pc2 = intcode('./input')
    pc3 = intcode('./input')
    pc4 = intcode('./input')
    pc5 = intcode('./input')
    
    for i in permutate(list('56789')):
        stack.append(i[0])
        pc1.execute()
        stack.append(i[1])
        pc2.execute()
        stack.append(i[2])
        pc3.execute()
        stack.append(i[3])
        pc4.execute()
        stack.append(i[4])
        pc5.execute()
        
        Done = False
        while(Done != True):
            pc1.execute()
            pc2.execute()
            pc3.execute()
            pc4.execute()
            Done = pc5.execute()
            
        solutions[str(i)] = int(stack.pop())
        
        stack.append(0)
            
        pc1.reset_program()
        pc2.reset_program()
        pc3.reset_program()
        pc4.reset_program()
        pc5.reset_program()
        
    print("Answer = %i" % max(solutions.values()))
        
    