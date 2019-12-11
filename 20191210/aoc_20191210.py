f = open("input.txt", 'r')
mainmap = f.read().lstrip().rstrip()
f.close()


map1 = """
.#..#
.....
#####
....#
...##
""".lstrip().rstrip()


map2 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""".lstrip().rstrip()


map3 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""".lstrip().rstrip()


map4 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""".lstrip().rstrip()


map5 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""".lstrip().rstrip()


class Asteroid():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.visible = {}
        self.alive = True

    def findVisible(self, asteroids=[]):
        self.visible = {}
        for asteroid in asteroids:
            if asteroid.alive:
                vector = (asteroid.x-self.x, asteroid.y-self.y)
                vector, factor = self.unitVectorize(vector)
                if vector in self.visible.keys():
                    self.visible[vector][factor] = asteroid
                else:
                    self.visible[vector] = {factor: asteroid}

        return len(self.visible.keys())-1
        #print("Asteroid ", self.x, self.y, len(self.visible.keys())-1)

    def unitVectorize(self, vector):
        if vector[0] == 0 and vector[1] == 0:
            return (0,0), 1

        xsign = 1
        ysign = 1
        if vector[0] < 0:
            xsign = -1
        if vector[1] < 0:
            ysign = -1

        if vector[0] == 0:
            return (0,ysign), 1
        if vector[1] == 0:
            return (xsign,0), 1

        vector = (abs(vector[0]), abs(vector[1]))

        xfactors = []
        for i in range(1, vector[0]+1):
            if float(vector[0]/i) == int(vector[0]/i):
                xfactors.append(i)

        xfactors.reverse()

        for factor in xfactors:
            if float(vector[1]/factor) == int(vector[1]/factor):
                return ((int(vector[0]/factor)*xsign, int(vector[1]/factor)*ysign)), factor


def part1(map):
    maplines = map.split('\n')

    asteroids = []

    for i, line in enumerate(maplines):
        for j in range(len(line)):
            if maplines[i][j] == "#":
                asteroids.append(Asteroid(x=j, y=i))

    maxcount = 0
    baseasteroid = None

    for asteroid in asteroids:
        count = asteroid.findVisible(asteroids)
        if count > maxcount:
            print(count)
            maxcount = count
            baseasteroid = asteroid

    print("Asteroid: ", baseasteroid.x, baseasteroid.y)
    print("Count: ", maxcount)

#part1(mainmap)

def part2(map):
    maplines = map.split('\n')

    asteroids = []

    for i, line in enumerate(maplines):
        for j in range(len(line)):
            if maplines[i][j] == "#":
                asteroids.append(Asteroid(x=j, y=i))

    maxcount = 0
    baseasteroid = None

    for asteroid in asteroids:
        count = asteroid.findVisible(asteroids)
        if count > maxcount:
            #print(count)
            maxcount = count
            baseasteroid = asteroid

    killcount = 0
    totalcount = map.count('#')

    while killcount+1 < totalcount:
        baseasteroid.findVisible(asteroids)
        angles = [{}, {}, {}, {}]

        for vector in baseasteroid.visible.keys():
            if vector[0] >= 0 and vector[1] < 0:
                angles[0][vector[0] / vector[1]] = vector
            if vector[0] > 0 and vector[1] >= 0:
                angles[1][vector[1] / vector[0]] = vector
            if vector[0] <= 0 and vector[1] > 0:
                angles[2][vector[0] / vector[1]] = vector
            if vector[0] < 0 and vector[1] <= 0:
                angles[3][vector[1] / vector[0]] = vector


        quadrants = [[], [], [], []]
        for i in range(4):
            for angle in angles[i].keys():
                quadrants[i].append(angle)
            quadrants[i].sort()
            if i == 0 or i == 2:
                quadrants[i].reverse()

            for angle in quadrants[i]:
                first = min(baseasteroid.visible[angles[i][angle]].keys())
                destroid = baseasteroid.visible[angles[i][angle]][first]
                destroid.alive = False
                killcount += 1
                print("Number ", killcount, " at ", destroid.x, destroid.y)

    print("Everything else is now spacedust")

part2(mainmap)
