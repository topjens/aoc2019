#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:25:06 2019

@author: jens
"""

class intcode:   
    def __init__(self, program):
        with open(program) as file:
            self.memory = file.readline()

        self.memory = self.memory.split(',')
        self.memory = list(map(int, self.memory))
        self.original_memory = self.memory.copy()

        self.pc = 0
        self.halt = False

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
        par1 = self.memory[self.pc+1]
        self.memory[par1] = int(input())

    def do_output(self):
        par1 = self.memory[self.pc+1]
        if(self.par1_mode == 0):
            par1 = self.memory[par1]

        print(par1)

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

    def do_halt(self):
        print("HALT")
        self.halt = True

    def untangle_instruction(self, instruction):
        instruction = [int(i) for i in str(instruction)]
        
        while(len(instruction) != 5):
            instruction.insert(0, 0)
            
        self.par1_mode = instruction[2]
        self.par2_mode = instruction[1]
        self.par3_mode = instruction[0]

        return instruction[3]*10+instruction[4]

    def execute(self):
        while(self.halt == False):
            instruction = self.memory[self.pc]
            instruction = self.untangle_instruction(instruction)
            self.opcodes[instruction]()
            self.pc += self.opcode_size[instruction]
            
if __name__ == '__main__':
    pc1 = intcode('./input')
    pc1.execute()
