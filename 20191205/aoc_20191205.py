OPCODE_HALT = 99
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JIT = 5
OPCODE_JIF = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUALS = 8

MODE_PARAMETER = 0
MODE_IMMEDIATE = 1

f = open("input.txt", 'r')
rawdata = f.read().split(',')
f.close()

in0 = 1

program1 = [3,0,4,0,99]
in1 = 10
out1 = 0

program2 = [1002,4,3,4,33]

program3 = [3,9,8,9,10,9,4,9,99,-1,8]
program4 = [3,9,7,9,10,9,4,9,99,-1,8]
program5 = [3,3,1108,-1,8,3,4,3,99]
program6 = [3,3,1107,-1,8,3,4,3,99]
program7 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
program8 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
program9 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
            999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

def RunIntCodeProgram(inp=0, outp=0, data=[]):
    data = [int(x) for x in data]
    sp = 0
    op = 0

    inp = inp
    out = outp
    alive = True

    while alive:
        op = data[sp]
        if op == OPCODE_HALT:
            #print("Finished")
            alive = False
            continue

        op = '{:0>3}'.format(int(op))

        if int(op[-1]) == OPCODE_INPUT:
            sp, data = opcodeInput(sp, data, inp, mode=op)
            continue
        elif int(op[-1]) == OPCODE_OUTPUT:
            sp, out = opcodeOutput(sp, data, mode=op)
            continue

        op = '{:0>4}'.format(int(op))

        if int(op[-1]) == OPCODE_JIT:
            sp = opcodeJIT(sp, data, mode=op)
            continue
        elif int(op[-1]) == OPCODE_JIF:
            sp = opcodeJIF(sp, data, mode=op)
            continue

        op = '{:0>5}'.format(int(op))

        if int(op[-1]) == OPCODE_ADD:
            sp, data = opcodeAdd(sp, data, mode=op)
            continue
        elif int(op[-1]) == OPCODE_MULTIPLY:
            sp, data = opcodeMultiply(sp, data, mode=op)
            continue
        elif int(op[-1]) == OPCODE_LESSTHAN:
            sp, data = opcodeLessThan(sp, data, mode=op)
            continue
        elif int(op[-1]) == OPCODE_EQUALS:
            sp, data = opcodeEquals(sp, data, mode=op)
            continue

        else:
            print("Something went wrong")

    return inp, out, data

def opcodeAdd(sp=0, data=[], mode="000"):
    mode = '{:0>5}'.format(int(mode))

    sp += 1
    reg1 = data[sp]
    if int(mode[2]) == MODE_PARAMETER:
        reg1 = data[reg1]

    sp += 1
    reg2 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg2 = data[reg2]

    sp += 1
    dest = data[sp]
    if int(mode[0]) == MODE_PARAMETER:
        data[dest] = reg1 + reg2
    else:
        data[sp] = reg1 + reg2

    sp += 1
    return sp, data

def opcodeMultiply(sp=0, data=[], mode="000"):
    mode = '{:0>5}'.format(int(mode))

    sp += 1
    reg1 = data[sp]
    if int(mode[2]) == MODE_PARAMETER:
        reg1 = data[reg1]

    sp += 1
    reg2 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg2 = data[reg2]

    sp += 1
    dest = data[sp]
    if int(mode[0]) == MODE_PARAMETER:
        data[dest] = reg1 * reg2
    else:
        data[sp] = reg1 * reg2

    sp += 1
    return sp, data

def opcodeInput(sp=0, data=[], inp=0, mode="00"):
    mode = '{:0>3}'.format(int(mode))
    sp += 1
    reg1 = data[sp]

    if int(mode[0]) == MODE_PARAMETER:
        data[reg1] = inp
    else:
        data[sp] = inp

    sp += 1
    return sp, data

def opcodeOutput(sp=0, data=[], mode="00"):
    mode = '{:0>3}'.format(int(mode))
    sp += 1
    reg1 = data[sp]

    if int(mode[0]) == MODE_PARAMETER:
        reg1 = data[reg1]

    out = reg1

    sp += 1
    return sp, out

def opcodeJIT(sp=0, data=[], mode="00"):
    mode = '{:0>4}'.format(int(mode))

    sp += 1

    reg1 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg1 = data[reg1]

    if reg1 != 0:
        sp += 1
        reg1 = data[sp]

        if int(mode[0]) == MODE_PARAMETER:
            reg1 = data[reg1]

        sp = reg1

    else:
        sp += 2

    return sp


def opcodeJIF(sp=0, data=[], mode="00"):
    mode = '{:0>4}'.format(int(mode))

    sp += 1

    reg1 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg1 = data[reg1]

    if reg1 == 0:
        sp += 1
        reg1 = data[sp]

        if int(mode[0]) == MODE_PARAMETER:
            reg1 = data[reg1]

        sp = reg1

    else:
        sp += 2

    return sp

def opcodeLessThan(sp=0, data=[], mode="00"):
    mode = '{:0>5}'.format(int(mode))

    sp += 1
    reg1 = data[sp]
    if int(mode[2]) == MODE_PARAMETER:
        reg1 = data[reg1]

    sp += 1
    reg2 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg2 = data[reg2]

    sp += 1
    dest = data[sp]
    if int(mode[0]) == MODE_PARAMETER:
        data[dest] = int(reg1 < reg2)
    else:
        data[sp] = int(reg1 < reg2)

    sp += 1
    return sp, data


def opcodeEquals(sp=0, data=[], mode="00"):
    mode = '{:0>5}'.format(int(mode))

    sp += 1
    reg1 = data[sp]
    if int(mode[2]) == MODE_PARAMETER:
        reg1 = data[reg1]

    sp += 1
    reg2 = data[sp]
    if int(mode[1]) == MODE_PARAMETER:
        reg2 = data[reg2]

    sp += 1
    dest = data[sp]
    if int(mode[0]) == MODE_PARAMETER:
        data[dest] = int(reg1 == reg2)
    else:
        data[sp] = int(reg1 == reg2)

    sp += 1
    return sp, data


inp1, out1, program1 = RunIntCodeProgram(inp=5, outp=out1, data=rawdata)

print("In", inp1)
print("Out", out1)
print(program1)