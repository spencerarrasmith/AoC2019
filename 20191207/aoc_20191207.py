import threading, time

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
ampprogram = f.read().split(',')
f.close()

class IntCodeComputer():
    def __init__(self, inputs=[], program=[]):
        self.inputs = [int(x) for x in inputs]
        self.mostrecentinput = None

        self.program = program
        self.program = [int(x) for x in self.program]

        self.sp = 0     # Stack pointer
        self.alive = threading.Event()

        self.outputs = []
        self.running = False

    def loadProgram(self, program):
        self.program = [int(x) for x in program]
        self.sp = 0

    def loadInputs(self, inputs):
        self.inputs = [int(x) for x in inputs]

    def queueInput(self, input):
        if input != None:
            self.mostrecentinput = int(input)
            self.inputs.append(int(input))

    def readOutput(self):
        if len(self.outputs):
            out = self.outputs.pop(0)
            #print(out)
            return out
        else:
            return None

    def run(self):
        self.prog_thread = threading.Thread(target=self.thread_program)
        self.prog_thread.setDaemon(1)
        self.alive.set()
        self.prog_thread.start()

    def thread_program(self):
        self.running = True
        while self.alive.isSet():
            op = self.program[self.sp]
            if op == OPCODE_HALT:
                self.running = False
                self.alive.clear()
                continue

            op = '{:0>3}'.format(int(op))

            if int(op[-1]) == OPCODE_INPUT:
                while not len(self.inputs):
                    time.sleep(0.001)
                    pass
                self.sp, self.program = self.opcodeInput(sp=self.sp, data=self.program, inp=self.inputs.pop(0), mode=op)
                continue
            elif int(op[-1]) == OPCODE_OUTPUT:
                self.sp, out = self.opcodeOutput(self.sp, self.program, mode=op)
                self.outputs.append(out)
                continue

            op = '{:0>4}'.format(int(op))

            if int(op[-1]) == OPCODE_JIT:
                self.sp = self.opcodeJIT(self.sp, self.program, mode=op)
                continue
            elif int(op[-1]) == OPCODE_JIF:
                self.sp = self.opcodeJIF(self.sp, self.program, mode=op)
                continue

            op = '{:0>5}'.format(int(op))

            if int(op[-1]) == OPCODE_ADD:
                self.sp, self.program = self.opcodeAdd(self.sp, self.program, mode=op)
                continue
            elif int(op[-1]) == OPCODE_MULTIPLY:
                self.sp, self.program = self.opcodeMultiply(self.sp, self.program, mode=op)
                continue
            elif int(op[-1]) == OPCODE_LESSTHAN:
                self.sp, self.program = self.opcodeLessThan(self.sp, self.program, mode=op)
                continue
            elif int(op[-1]) == OPCODE_EQUALS:
                self.sp, self.program = self.opcodeEquals(self.sp, self.program, mode=op)
                continue

            else:
                print("Something went wrong")

        return

    def opcodeAdd(self, sp=0, data=[], mode="000"):
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

    def opcodeMultiply(self, sp=0, data=[], mode="000"):
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

    def opcodeInput(self, sp=0, data=[], inp=0, mode="00"):
        mode = '{:0>3}'.format(int(mode))
        sp += 1
        reg1 = data[sp]

        if int(mode[0]) == MODE_PARAMETER:
            data[reg1] = inp
        else:
            data[sp] = inp

        sp += 1
        return sp, data

    def opcodeOutput(self, sp=0, data=[], mode="00"):
        mode = '{:0>3}'.format(int(mode))
        sp += 1
        reg1 = data[sp]

        if int(mode[0]) == MODE_PARAMETER:
            reg1 = data[reg1]

        out = reg1

        sp += 1
        return sp, out

    def opcodeJIT(self, sp=0, data=[], mode="00"):
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

    def opcodeJIF(self, sp=0, data=[], mode="00"):
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

    def opcodeLessThan(self, sp=0, data=[], mode="00"):
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

    def opcodeEquals(self, sp=0, data=[], mode="00"):
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

program9 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
            999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

ampprogram1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
phasesequence1 = [4,3,2,1,0]

ampprogram2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
phasesequence2 = [0,1,2,3,4]

ampprogram3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
phasesequence3 = [1,0,4,3,2]





MyIntCodeComputer = IntCodeComputer()

def part1():
    out = 0
    maxsignal = 0
    maxphase = []
    phasesequences = []

    for i in range(5):
        for j in range(5):
            for k in range(5):
                for l in range(5):
                    for m in range(5):
                        phasesequence = [i,j,k,l,m]
                        if len(set(phasesequence)) == len(phasesequence):
                            phasesequences.append(phasesequence)

    for phasesequence in phasesequences:
        out = 0
        for phase in phasesequence:
            MyIntCodeComputer.loadInputs([phase, out])
            MyIntCodeComputer.loadProgram(ampprogram)
            MyIntCodeComputer.run()
            out = MyIntCodeComputer.readOutput()
            if out > maxsignal:
                maxsignal = out
                maxphase = phasesequence

    print("Signal: ", maxsignal)


feedbackprogram1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
feedbackphase1 = [9,8,7,6,5]

feedbackprogram2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
feedbackphase2 = [9,7,8,5,6]

def part2():
    out = 0
    maxsignal = 0
    maxphase = []
    phasesequences = []

    for i in range(5,10):
        for j in range(5,10):
            for k in range(5,10):
                for l in range(5,10):
                    for m in range(5,10):
                        phasesequence = [i,j,k,l,m]
                        if len(set(phasesequence)) == len(phasesequence):
                            phasesequences.append(phasesequence)

    for phasesequence in phasesequences:
        Amps = [IntCodeComputer() for x in range(5)]
        for i, Amp in enumerate(Amps):
            Amp.loadProgram(ampprogram)
            Amps[i].queueInput(phasesequence[i])
            Amp.run()

        Amps[0].queueInput(0)

        while Amps[0].running or Amps[1].running or Amps[2].running or Amps[3].running or Amps[4].running:
            for i in range(len(Amps)):
                Amps[i].queueInput(Amps[i - 1].readOutput())

        out1 = Amps[0].mostrecentinput
        out2 = Amps[4].readOutput()

        if out2 != None:
            if max([out1, out2]) > maxsignal:
                maxsignal = max([out1, out2])
        else:
            if out1 > maxsignal:
                maxsignal = out1
        print(phasesequence, maxsignal)

    print("Signal: ", maxsignal)

def part2Test():
    Amps = [IntCodeComputer() for x in range(5)]
    for i,Amp in enumerate(Amps):
        Amp.loadProgram(feedbackprogram2)
        Amps[i].queueInput(feedbackphase2[i])
        Amp.run()

    Amps[0].queueInput(0)

    while Amps[0].running or Amps[1].running or Amps[2].running or Amps[3].running or Amps[4].running:
        for i in range(len(Amps)):
            Amps[i].queueInput(Amps[i-1].readOutput())

    out1 = Amps[0].mostrecentinput
    out2 = Amps[4].readOutput()

    if out2 != None:
        print("Out: ", max([out1, out2]))
    else:
        print("Out: ", out1)


part2()