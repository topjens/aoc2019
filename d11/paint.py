#!/bin/python

# the mnemonics with their opcode
ADD  = 1
MUL  = 2
IN   = 3
OUT  = 4
JT   = 5
JF   = 6
LESS = 7
EQU  = 8
ADB  = 9
HLT  = 99

# operands can be either read or write
READ  = 0
WRITE = 1

# operands can be given in 3 modes
POSITION  = 0
IMMEDIATE = 1
RELATIVE  = 2

# directions
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

class robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = UP
        self.movecount = 0

        self.board = {(0,0): 1}

    def move(self, direction, color):
        self.movecount += 1
        self.board[(self.x,self.y)] = color
        if direction == 0:
            self.direction += 1
            if self.direction > RIGHT:
                self.direction = UP
        elif direction == 1:
            self.direction -= 1
            if self.direction < UP:
                self.direction = RIGHT
        else:
            raise Exception("%i: Illegal direction %i!" % (self.movecount, direction))

        if self.direction == UP:
            self.y += 1
        elif self.direction == LEFT:
            self.x -= 1
        elif self.direction == DOWN:
            self.y -= 1
        elif self.direction == RIGHT:
            self.x += 1

    def print_board(self):
        print(self.board)

    def read_camera(self):
        if (self.x, self.y) in self.board:
            #print("Camera says %i" % self.board[(self.x, self.y)])
            return self.board[(self.x, self.y)]
        
        else:
            #print("Camera says nothing")
            return 0
    def render(self, filename = None):
        xmin = min([x for (x,y) in self.board])
        ymin = min([y for (x,y) in self.board])
        xmax = max([x for (x,y) in self.board])
        ymax = max([y for (x,y) in self.board])

        if(filename != None):
            with open(filename, 'w') as file:
                file.write('P1\n')
                file.write('# Solution of day 11 of AOC 2019\n')
                file.write('%i %i\n' % (xmax-xmin+1, ymax-ymin+1))
                
                for y in range(ymin, ymax + 1):
                    for x in range(xmin, xmax + 1):
                        if (x,y) in self.board:
                            file.write(str(self.board[(x,y)]) + ' ')
                        else:
                            file.write('0 ')
                    file.write('\n')

        else:
            for y in range(ymin, ymax + 1):
                for x in range(xmin, xmax + 1):
                    if (x,y) in self.board:
                        pixel = self.board[(x,y)]
                        if(pixel == 0):
                            print(".", end="")
                        else:
                            print("#", end="")
                    else:
                        print(".", end="")
                print()

class intcode:
    def __init__(self, program):
        with open(program) as file:
            self.memory = file.readline()

        self.memory = self.memory.split(',')
        self.memory = list(map(int, self.memory))
        self.original_memory = self.memory.copy()

        self.stack = []

        self.r = robot()

        self.pc = 0
        self.rb = 0

        self.opcodes = {
            ADD:  (READ, READ, WRITE),
            MUL:  (READ, READ, WRITE),
            IN:   (WRITE,),
            OUT:  (READ,),
            JT:   (READ, READ),
            JF:   (READ, READ),
            LESS: (READ, READ, WRITE),
            EQU:  (READ, READ, WRITE),
            ADB:  (READ,),
            HLT:  (),
        }
        
    def reset_program(self):
        self.memory = self.original_memory.copy()
        self.pc = 0
        self.rb = 0
        self.r = robot()

    def untangle_instruction(self, opcode, modes):
        ret = [None] * 3

        if opcode not in self.opcodes:
            raise Exception("Unknown opcode %i!" % opcode)

        for i, type in enumerate(self.opcodes[opcode]):
            mode = modes % 10
            modes //= 10
            mem = self.memory[self.pc + 1 + i]
            
            if mode == RELATIVE:
                mem += self.rb

            if mode == RELATIVE or mode == POSITION:
                if mem < 0:
                    raise Exception("Cannot write to negative address!")
                if mem >= len(self.memory):
                    self.memory += [0] * (mem - len(self.memory) + 1)
                if type == READ:
                    mem = self.memory[mem]
                elif type != WRITE:
                    raise Exception("Unknown operand type %i" % type)

            elif(mode == IMMEDIATE):
                if(type == WRITE):
                    raise Exception("Immediate mode not allowed for write operands!")

            ret[i] = mem

        self.pc += 1 + len(self.opcodes[opcode])

        return ret

    def execute(self):
        while(self.memory[self.pc] != HLT):
            instruction = self.memory[self.pc]

            opcode = instruction % 100
            modes = instruction // 100
            op1, op2, op3 = self.untangle_instruction(opcode, modes)

            if opcode == ADD:
                self.memory[op3] = op1 + op2
            elif opcode == MUL:
                self.memory[op3] = op1 * op2
            elif opcode == IN:
                if(len(self.stack) > 1):
                    self.r.move(self.stack.pop(), self.stack.pop())
                self.memory[op1] = self.r.read_camera()
            elif opcode == OUT:
                self.stack.append(op1)
            elif opcode == JT:
                if op1 != 0:
                    self.pc = op2
            elif opcode == JF:
                if op1 == 0:
                    self.pc = op2
            elif opcode == LESS:
                if op1 < op2:
                    self.memory[op3] = 1
                else:
                    self.memory[op3] = 0
            elif opcode == EQU:
                if op1 == op2:
                    self.memory[op3] = 1
                else:
                    self.memory[op3] = 0
            elif opcode == ADB:
                self.rb += op1
            else:
                raise Exception("Unknown opcode %i!" % opcode)
        self.r.print_board()
        self.r.render("part2.pbm")
        print(len(self.r.board))


if __name__ == '__main__':
    r = robot()
    intcode('./input').execute()
