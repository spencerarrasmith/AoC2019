# --- Day 12: The N-Body Problem ---
#
#   Part 1: Control painting and movement of robot with IntCode computer
#   Part 2: Read text painted by robot
#

names = ["Io", "Europa", "Ganymede", "Callisto"]

f = open("input.txt", 'r')
inputs = f.read().strip().split('\n')
f.close()

# test1 = """
# <x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>
# """.strip().split('\n')
#
# test2 = """
# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
# """.strip().split('\n')



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

        self.pe = self.loc.e
        self.ke = 0
        self.te = 0

    def gravitate(self, moons=[]):
        for moon in moons:
            if moon != self:
                for i,element in enumerate(moon.loc):
                    if element > self.loc[i]:
                        self.vel[i] += 1
                    elif element < self.loc[i]:
                        self.vel[i] -= 1

    def velocitate(self):
        for i, element in enumerate(self.vel):
            self.loc[i] += element
        self.pe = self.loc.e
        self.ke = self.vel.e
        self.te = self.pe * self.ke

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

part1(inputs)