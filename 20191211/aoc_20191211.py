import threading, time
from PIL import Image

OPCODE_HALT = 99
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JIT = 5
OPCODE_JIF = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUALS = 8
OPCODE_RELATIVEBASE = 9

MODE_PARAMETER = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

f = open("input.txt", 'r')
mainprogram = f.read().split(',')
f.close()

class IntCodeComputer():
    def __init__(self, inputs=[], program=[], threaded=False):
        self.inputs = [int(x) for x in inputs]
        self.mostrecentinput = None

        self.program = program
        self.program = [int(x) for x in self.program]

        self.threaded = threaded        # Run program loop in a separate thread
        self.sp = 0                     # Stack pointer
        self.rb = 0                     # Relative base for relative mode
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
        if self.threaded:
            self.prog_thread.start()
        else:
            self.thread_program()


    def thread_program(self):
        self.running = True
        while self.alive.isSet():
            valid, op = self.readMemory(self.sp)
            if op == OPCODE_HALT or valid == False:
                self.running = False
                self.alive.clear()
                continue

            op = '{:0>3}'.format(int(op))

            if int(op[-1]) == OPCODE_INPUT:
                while not len(self.inputs):
                    time.sleep(0.001)
                    pass
                self.opcodeInput(inp=self.inputs.pop(0), mode=op)
                continue
            elif int(op[-1]) == OPCODE_OUTPUT:
                out = self.opcodeOutput(mode=op)
                self.outputs.append(out)
                continue
            elif int(op[-1]) == OPCODE_RELATIVEBASE:
                self.opcodeRelativeBase(mode=op)
                continue

            op = '{:0>4}'.format(int(op))

            if int(op[-1]) == OPCODE_JIT:
                self.opcodeJIT(mode=op)
                continue
            elif int(op[-1]) == OPCODE_JIF:
                self.opcodeJIF(mode=op)
                continue

            op = '{:0>5}'.format(int(op))

            if int(op[-1]) == OPCODE_ADD:
                self.opcodeAdd(mode=op)
                continue
            elif int(op[-1]) == OPCODE_MULTIPLY:
                self.opcodeMultiply(mode=op)
                continue
            elif int(op[-1]) == OPCODE_LESSTHAN:
                self.opcodeLessThan(mode=op)
                continue
            elif int(op[-1]) == OPCODE_EQUALS:
                self.opcodeEquals(mode=op)
                continue

            else:
                print("Something went wrong")

        return


    def readMemory(self, p):
        if p < 0:
            return False, None
        else:
            try:
                data = self.program[p]
                return True, data
            except IndexError:
                for i in range(p-len(self.program)+1):
                    self.program.append(0)
                return True, self.program[p]

    def writeMemory(self, p, data):
        if p < 0:
            return False
        else:
            try:
                self.program[p] = data
                return True
            except IndexError:
                for i in range(p-len(self.program)+1):
                    self.program.append(0)
                self.program[p] = data
                return True

    def opcodeAdd(self, mode="000"):
        mode = '{:0>5}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[2]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[2]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 3
            return

        self.sp += 1
        valid, reg2 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg2 = self.readMemory(reg2)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg2 = self.readMemory(reg2 + self.rb)

        if not valid:
            self.sp += 2
            return

        self.sp += 1
        valid, dest = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid = self.writeMemory(dest, reg1 + reg2)
        elif int(mode[0]) == MODE_IMMEDIATE:
            valid = self.writeMemory(self.sp, reg1 + reg2)
        elif int(mode[0]) == MODE_RELATIVE:
            valid = self.writeMemory(dest + self.rb, reg1 + reg2)
        else:
            valid = False

        self.sp += 1
        return

    def opcodeMultiply(self, mode="000"):
        mode = '{:0>5}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[2]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[2]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 3
            return

        self.sp += 1
        valid, reg2 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg2 = self.readMemory(reg2)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg2 = self.readMemory(reg2 + self.rb)

        if not valid:
            self.sp += 2
            return

        self.sp += 1
        valid, dest = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid = self.writeMemory(dest, reg1 * reg2)
        elif int(mode[0]) == MODE_IMMEDIATE:
            valid = self.writeMemory(self.sp, reg1 * reg2)
        elif int(mode[0]) == MODE_RELATIVE:
            valid = self.writeMemory(dest + self.rb, reg1 * reg2)
        else:
            valid = False

        self.sp += 1
        return

    def opcodeInput(self, inp=0, mode="00"):
        mode = '{:0>3}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid = self.writeMemory(reg1, inp)
        elif int(mode[0]) == MODE_IMMEDIATE:
            valid = self.writeMemory(self.sp, inp)
        elif int(mode[0]) == MODE_RELATIVE:
            valid = self.writeMemory(reg1 + self.rb, inp)
        else:
            valid = False

        self.sp += 1
        return

    def opcodeOutput(self, mode="00"):
        mode = '{:0>3}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[0]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 1
            return None

        self.sp += 1
        return reg1

    def opcodeJIT(self, mode="00"):
        mode = '{:0>4}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 2
            return

        if reg1 != 0:
            self.sp += 1
            valid, reg1 = self.readMemory(self.sp)
            if int(mode[0]) == MODE_PARAMETER:
                valid, reg1 = self.readMemory(reg1)
            elif int(mode[0]) == MODE_RELATIVE:
                valid, reg1 = self.readMemory(reg1 + self.rb)

            if valid:
                self.sp = reg1
                return
            else:
                self.sp += 1
                return

        else:
            self.sp += 2
            return

    def opcodeJIF(self, mode="00"):
        mode = '{:0>4}'.format(int(mode))
        valid = False
        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 2
            return

        if reg1 == 0:
            self.sp += 1
            valid, reg1 = self.readMemory(self.sp)
            if int(mode[0]) == MODE_PARAMETER:
                valid, reg1 = self.readMemory(reg1)
            elif int(mode[0]) == MODE_RELATIVE:
                valid, reg1 = self.readMemory(reg1 + self.rb)

            if valid:
                self.sp = reg1
                return
            else:
                self.sp += 1
                return

        else:
            self.sp += 2

    def opcodeLessThan(self, mode="00"):
        mode = '{:0>5}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[2]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[2]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 3
            return

        self.sp += 1
        valid, reg2 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg2 = self.readMemory(reg2)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg2 = self.readMemory(reg2 + self.rb)

        if not valid:
            self.sp += 2
            return

        self.sp += 1
        valid, dest = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid = self.writeMemory(dest, int(reg1 < reg2))
        elif int(mode[0]) == MODE_IMMEDIATE:
            valid = self.writeMemory(self.sp, int(reg1 < reg2))
        elif int(mode[0]) == MODE_RELATIVE:
            valid = self.writeMemory(dest + self.rb, int(reg1 < reg2))
        else:
            valid = False

        self.sp += 1
        return

    def opcodeEquals(self, mode="00"):
        mode = '{:0>5}'.format(int(mode))
        valid = False

        self.sp += 1
        valid, reg1 = self.readMemory(self.sp)
        if int(mode[2]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[2]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if not valid:
            self.sp += 3
            return

        self.sp += 1
        valid, reg2 = self.readMemory(self.sp)
        if int(mode[1]) == MODE_PARAMETER:
            valid, reg2 = self.readMemory(reg2)
        elif int(mode[1]) == MODE_RELATIVE:
            valid, reg2 = self.readMemory(reg2 + self.rb)

        if not valid:
            self.sp += 2
            return

        self.sp += 1
        valid, dest = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid = self.writeMemory(dest, int(reg1 == reg2))
        elif int(mode[0]) == MODE_IMMEDIATE:
            valid = self.writeMemory(self.sp, int(reg1 == reg2))
        elif int(mode[0]) == MODE_RELATIVE:
            valid = self.writeMemory(dest + self.rb, int(reg1 == reg2))
        else:
            valid = False

        self.sp += 1

    def opcodeRelativeBase(self, mode="00"):
        mode = '{:0>3}'.format(int(mode))
        valid = False

        self.sp += 1

        valid, reg1 = self.readMemory(self.sp)
        if int(mode[0]) == MODE_PARAMETER:
            valid, reg1 = self.readMemory(reg1)
        elif int(mode[0]) == MODE_RELATIVE:
            valid, reg1 = self.readMemory(reg1 + self.rb)

        if valid:
            self.rb += reg1

        self.sp += 1
        return


class HullPainterBot():
    def __init__(self):
        self.rotation = 0
        self.x = 0
        self.y = 0

        self.xmax = 0
        self.xmin = 0
        self.ymax = 0
        self.ymin = 0

        self.paintedGrid = {}
        self.totalPainted = 0

    def paint(self, p):
        if (self.x, self.y) not in self.paintedGrid.keys():
            self.paintedGrid[(self.x, self.y)] = 0
        self.paintedGrid[(self.x, self.y)] = p
        if len(self.paintedGrid.keys()) != self.totalPainted:
            self.totalPainted = len(self.paintedGrid.keys())
            print(self.totalPainted)

    def move(self, r):
        if r == 0:
            r = -1
        self.rotation += r
        self.rotation %= 4

        if self.rotation == 0:
            self.y -= 1
        elif self.rotation == 1:
            self.x += 1
        elif self.rotation == 2:
            self.y += 1
        elif self.rotation == 3:
            self.x -= 1

        if self.x < self.xmin:
            self.xmin = self.x
        if self.x > self.xmax:
            self.xmax = self.x
        if self.y < self.ymin:
            self.ymin = self.y
        if self.y > self.ymax:
            self.ymax = self.y

        if (self.x, self.y) in self.paintedGrid.keys():
            return self.paintedGrid[(self.x, self.y)]
        else:
            return 0



ICC = IntCodeComputer(threaded=True)

ICC.loadProgram(program=mainprogram)
ICC.loadInputs(inputs=[1])
ICC.run()

HPB = HullPainterBot()

i = 0
inputs = []

while ICC.running:
    out = ICC.readOutput()
    if out != None:
        #print(out)
        if i%2 == 0:
            HPB.paint(out)
            i += 1
        else:
            inp = HPB.move(out)
            inputs.append(inp)
            i += 1

    if len(inputs):
        inp = inputs.pop(0)
        ICC.loadInputs(inputs=[inp])


img = Image.new('RGB', (abs(HPB.xmin) + abs(HPB.xmax) + 2, abs(HPB.ymin) + abs(HPB.ymax) + 2), "black")
pixels = img.load()

for pixel in HPB.paintedGrid.keys():
    pixelx = pixel[0]-HPB.xmin
    pixely = pixel[1]-HPB.ymin
    value = 255*HPB.paintedGrid[pixel]
    pixels[pixelx, pixely] = (value, value, value)

img.save("part2.png")