# --- Day 12: The N-Body Problem ---
#
#   Part 1: Control painting and movement of robot with IntCode computer
#   Part 2: Read text painted by robot
#

import time

names = ["Io", "Europa", "Ganymede", "Callisto"]

f = open("input.txt", 'r')
inputs = f.read().strip().split('\n')
f.close()

test1 = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')

test2 = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""".strip().split('\n')



class Vector(list):
    def __init__(self, x=0, y=0, z=0):
        self.append(x)
        self.append(y)
        self.append(z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, val):
        self[0] = val
        return

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, val):
        self[1] = val
        return

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, val):
        self[2] = val
        return

    @property
    def e(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon():
    def __init__(self, name="", loc=Vector(0,0,0)):
        self.name = name

        self.vel = Vector(0,0,0)
        self.loc = loc

        self.initialstate = [self.loc.copy(), self.vel.copy()]

        self.pe = self.loc.e
        self.ke = 0
        self.te = 0

    def gravitate(self, moons=[], axis=3):
        for moon in moons:
            if moon != self:
                if axis >= 3:   # All axes
                    for i,element in enumerate(moon.loc):
                        if element > self.loc[i]:
                            self.vel[i] += 1
                        elif element < self.loc[i]:
                            self.vel[i] -= 1
                else:   # Just the one axis
                    if moon.loc[axis] > self.loc[axis]:
                        self.vel[axis] += 1
                    elif moon.loc[axis] < self.loc[axis]:
                        self.vel[axis] -= 1

    def velocitate(self, axis=3):
        if axis == 3:   # All axes
            for i, element in enumerate(self.vel):
                self.loc[i] += element
            self.pe = self.loc.e
            self.ke = self.vel.e
            self.te = self.pe * self.ke
        else:   # Just the one axis
            self.loc[axis] += self.vel[axis]


def primeFactorize(num):
    current = num
    currentprime = 2
    factorization = []
    while current > 1:
        if currentprime > current/2:
            factorization.append(int(current))
            break
        if current % currentprime == 0:
            factorization.append(int(currentprime))
            current /= currentprime
            continue
        else:
            currentprime += 1
            while not isPrime(currentprime):
                currentprime += 1
    return factorization

def isPrime(num):
    for i in range(2,int(num+1/2)):
        if num % i == 0:
            return False
    return True

#print(primeFactorize(4702))


def part1(inputs):
    inputs = [x[1:-1].split(',') for x in inputs]
    for i, line in enumerate(inputs):
        inputs[i] = [int(elt.split('=')[1]) for elt in line]
    #print(inputs)

    Moons = []

    for i, name in enumerate(names):
        Moons.append(Moon(name=name, loc=Vector(inputs[i][0], inputs[i][1], inputs[i][2])))


    for i in range(1000):
        for moon in Moons:
            moon.gravitate(Moons)
        for moon in Moons:
            moon.velocitate()
            #print(moon.loc, moon.vel, moon.pe, moon.ke, moon.te)
        #print("")

    print(Moons[0].te + Moons[1].te + Moons[2].te + Moons[3].te)

#part1(inputs)

def part2(inputs):
    inputs = [x[1:-1].split(',') for x in inputs]
    for i, line in enumerate(inputs):
        inputs[i] = [int(elt.split('=')[1]) for elt in line]
    #print(inputs)

    Moons = []


    for i, name in enumerate(names):
        Moons.append(Moon(name=name, loc=Vector(inputs[i][0], inputs[i][1], inputs[i][2])))

    looptimes = []

    for axis in range(3):
        initialstate = []

        currentaxis = axis

        for moon in Moons:
            initialstate.append(moon.loc[currentaxis])
            initialstate.append(moon.vel[currentaxis])

        print(initialstate)

        numsteps = 0
        currentstate = []

        while currentstate != initialstate:
            numsteps += 1
            currentstate = []
            for moon in Moons:
                moon.gravitate(Moons, axis=currentaxis)
            for moon in Moons:
                moon.velocitate(axis=currentaxis)
                currentstate.append(moon.loc[currentaxis])
                currentstate.append(moon.vel[currentaxis])


        print("Axis ", currentaxis, "Steps: ", numsteps)
        print("")
        looptimes.append(numsteps)

    primefactors = []
    for i in looptimes:
        primefactors.append(primeFactorize(i))

    lcmfactors = {}
    for factorlist in primefactors:
        for factor in set(factorlist):
            if factor not in lcmfactors.keys():
                lcmfactors[factor] = factorlist.count(factor)
            else:
                if lcmfactors[factor] < factorlist.count(factor):
                    lcmfactors[factor] = factorlist.count(factor)

    print(lcmfactors)

    lcm = 1
    for i in lcmfactors.keys():
        lcm *= i**lcmfactors[i]

    print(lcm)


part2(inputs)