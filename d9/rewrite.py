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

class intcode:
    def __init__(self, program):
        with open(program) as file:
            self.memory = file.readline()

        self.memory = self.memory.split(',')
        self.memory = list(map(int, self.memory))
        self.original_memory = self.memory.copy()

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
                print("> ", end = '')
                self.memory[op1] = int(input())
            elif opcode == OUT:
                print(op1)
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


if __name__ == '__main__':
    intcode('./test').execute()
