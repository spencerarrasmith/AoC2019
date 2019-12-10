OPCODE_HALT = 99
OPCODE_ADD = 1
OPCODE_MULTIPLY = 2

f = open("input.txt", 'r')
rawdata = f.read().split(',')
f.close()

#data = "1,9,10,3,2,3,11,0,99,30,40,50".split(",")
for noun in range(0,100):
    for verb in range(0,100):
        data = [int(x) for x in rawdata]

        data[1] = noun
        data[2] = verb

        #print(data)

        sp = 0
        op = 0
        reg1 = 0
        reg2 = 0
        dest = 0
        alive = True

        while alive:
            op = data[sp]
            if op == OPCODE_HALT:
                #print("Finished")
                alive = False
            elif op == OPCODE_ADD:
                sp += 1
                reg1 = data[sp]
                sp += 1
                reg2 = data[sp]
                sp += 1
                dest = data[sp]
                data[dest] = data[reg1] + data[reg2]
                sp += 1
            elif op == OPCODE_MULTIPLY:
                sp += 1
                reg1 = data[sp]
                sp += 1
                reg2 = data[sp]
                sp += 1
                dest = data[sp]
                data[dest] = data[reg1] * data[reg2]
                sp += 1
            else:
                print("Something went wrong")

        #print(data)
        if data[0] == 19690720:
            print(noun,verb)
            print(100 * noun + verb)