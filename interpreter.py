import sys

#read arguments
program_filepath = sys.argv[1]

#----------------------------------
#         Tokenize program
#----------------------------------

#read file lines
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    #check for empty line
    if opcode == "":
        continue

    #check for label
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    #store opcode token
    program.append(opcode)
    token_counter += 1

    #handle each opcode
    if opcode == "APPEND":
        #expecting a number
        number = int(parts[1])
        program.append(number)
        token_counter += 1

    elif opcode == "INSCRIBE":
        #parsing a string literal
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1

    elif opcode == "PROCEED.IF.EQ.0":
        #check for label =0
        label = parts[1]
        program.append(label)
        token_counter += 1

    elif opcode == "PROCEED.IF.GT.0":
        #check for label >0
        label = parts[1]
        program.append(label)
        token_counter += 1

#----------------------------------
#         Interpret program
#----------------------------------

class Stack:
    def __init__(self, size):
        #initialize
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        #push stack
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        #pop last element & return it
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        return self.buf[self.sp]


pc = 0
stack = Stack(256)

while program[pc] != "WITHHOLD":
    opcode = program[pc]
    pc += 1

    if opcode == "APPEND": #push element to stack
        number = program[pc]
        pc += 1
        stack.push(number)

    elif opcode == "DISPOSE": #remove element from stack
        stack.pop()

    elif opcode == "ADD": #pop two last elements and push their sum
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)

    elif opcode == "SUB": # pop two last elements and push their difference
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)

    elif opcode == "INSCRIBE": #print given string
        string_literal = program[pc]
        pc += 1
        print(string_literal)

    elif opcode == "READ": #ask for number input
        number = int(input())
        stack.push(number)

    elif opcode == "PROCEED.IF.EQ.0": #check if =0
        number = stack.top()
        if number == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1

    elif opcode == "PROCEED.IF.GT.0": #check if >0
        number = stack.top()
        if number > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
