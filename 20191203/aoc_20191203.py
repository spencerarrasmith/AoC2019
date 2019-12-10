import math
import time

start = time.time()

map = {}

def fillWire(map, x, y, wire):
    if (x,y,wire-1) in map.keys():
        map[(x,y,wire-1)] += 1
    else:
        map[(x,y,wire)] = 1

f = open("input.txt", 'r')
wires = f.read()
f.close()

wire1 = wires.split('\n')[0]
wire2 = wires.split('\n')[1]

#wire1 = 'R8,U5,L5,D3'
#wire2 = 'U7,R6,D4,L4'

#wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
#wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'

#wire1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
#wire2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'

wire1 = wire1.split(',')
wire2 = wire2.split(',')

mapx = 0
mapy = 0

fillWire(map, mapx, mapy, 1)

for segment in wire1:
    if segment[0] == 'U':
        for i in range(int(segment[1:])):
            mapy += 1
            fillWire(map, mapx, mapy, 1)
    if segment[0] == 'D':
        for i in range(int(segment[1:])):
            mapy -= 1
            fillWire(map, mapx, mapy, 1)
    if segment[0] == 'L':
        for i in range(int(segment[1:])):
            mapx -= 1
            fillWire(map, mapx, mapy, 1)
    if segment[0] == 'R':
        for i in range(int(segment[1:])):
            mapx += 1
            fillWire(map, mapx, mapy, 1)

mapx = 0
mapy = 0

fillWire(map, mapx, mapy, 2)

for segment in wire2:
    if segment[0] == 'U':
        for i in range(int(segment[1:])):
            mapy += 1
            fillWire(map, mapx, mapy, 2)
    if segment[0] == 'D':
        for i in range(int(segment[1:])):
            mapy -= 1
            fillWire(map, mapx, mapy, 2)
    if segment[0] == 'L':
        for i in range(int(segment[1:])):
            mapx -= 1
            fillWire(map, mapx, mapy, 2)
    if segment[0] == 'R':
        for i in range(int(segment[1:])):
            mapx += 1
            fillWire(map, mapx, mapy, 2)

mindist = 1000

for key in map:
    if map[key] >= 2:
        if abs(key[0]) + abs(key[1]) < mindist and abs(key[0]) + abs(key[1]) > 0:
            mindist = abs(key[0]) + abs(key[1])
            print(key)

print(mindist)

for key in map:
    if map[key] == 2:
        print(key)


# retrace the things
mapx = 0
mapy = 0
distance = 0
intersections1 = {}

for segment in wire1:
    if segment[0] == 'U':
        for i in range(int(segment[1:])):
            mapy += 1
            distance += 1
            if map[(mapx, mapy, 1)] == 2:
                intersections1[(mapx,mapy)] = distance
    if segment[0] == 'D':
        for i in range(int(segment[1:])):
            mapy -= 1
            distance += 1
            if map[(mapx, mapy, 1)] == 2:
                intersections1[(mapx,mapy)] = distance
    if segment[0] == 'L':
        for i in range(int(segment[1:])):
            mapx -= 1
            distance += 1
            if map[(mapx, mapy, 1)] == 2:
                intersections1[(mapx,mapy)] = distance
    if segment[0] == 'R':
        for i in range(int(segment[1:])):
            mapx += 1
            distance += 1
            if map[(mapx, mapy, 1)] == 2:
                intersections1[(mapx,mapy)] = distance


mapx = 0
mapy = 0
distance = 0
intersections2 = {}

for segment in wire2:
    if segment[0] == 'U':
        for i in range(int(segment[1:])):
            mapy += 1
            distance += 1
            if (mapx, mapy, 1) in map.keys():
                if map[(mapx, mapy, 1)] == 2:
                    intersections2[(mapx,mapy)] = distance
    if segment[0] == 'D':
        for i in range(int(segment[1:])):
            mapy -= 1
            distance += 1
            if (mapx, mapy, 1) in map.keys():
                if map[(mapx, mapy, 1)] == 2:
                    intersections2[(mapx,mapy)] = distance
    if segment[0] == 'L':
        for i in range(int(segment[1:])):
            mapx -= 1
            distance += 1
            if (mapx, mapy, 1) in map.keys():
                if map[(mapx, mapy, 1)] == 2:
                    intersections2[(mapx,mapy)] = distance
    if segment[0] == 'R':
        for i in range(int(segment[1:])):
            mapx += 1
            distance += 1
            if (mapx, mapy, 1) in map.keys():
                if map[(mapx, mapy, 1)] == 2:
                    intersections2[(mapx,mapy)] = distance


#print(intersections1)
#print(intersections2)
#print(intersection1 + intersection2)


firstintersection = 10000000

for key in intersections1:
    if intersections1[key] + intersections2[key] < firstintersection:
        firstintersection = intersections1[key] + intersections2[key]

print(firstintersection)

print(time.time() - start)