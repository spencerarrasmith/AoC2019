# --- Day 13: Care Package ---
#
#   Part 1: Use intcode computer to draw graphics, count bricks
#   Part 2: Play brick breaker with a joystick, calculate high score
#

import sys
sys.path.append("..")

import random, time
from PIL import Image

from AoCCommon.IntCodeComputer import IntCodeComputer

PIXELSCALE = 10

f = open("input.txt", 'r')
brickbreaker = f.read().split(',')
f.close()


class GameTile():
    def __init__(self, tileid=0, xdim=PIXELSCALE, ydim=PIXELSCALE):
        self.idname = ""
        self.color = (0,0,0)
        self.xdim = xdim
        self.ydim = ydim

        self.tileid = tileid

    @property
    def tileid(self):
        return self._tileid

    @tileid.setter
    def tileid(self, id):
        try:
            int(id)
        except:
            return
        self._tileid = id
        if id == 0:
            self.idname = "empty"
            self.color = (0,0,0)
        elif id == 1:
            self.idname = "wall"
            self.color=(150,150,150)
        elif id == 2:
            self.idname = "block"
            self.color=(200,120,120)
        elif id == 3:
            self.idname = "horizontal paddle"
            self.color=(120,120,200)
        elif id == 4:
            self.idname = "ball"
            self.color=(255,255,255)
        else:
            self.idname = "empty"
            self.color = (0, 0, 0)
            self._tileid = 0


class Screen(dict):
    def __init__(self, backgroundcolor=(0,0,0), *args, **kwargs):
        self.update(*args, **kwargs)

        self.xres = 0
        self._xmin = 0
        self._xmax = 0

        self.yres = 0
        self._ymin = 0
        self._ymax = 0

        self.backgroundcolor = backgroundcolor

    @property
    def xmin(self):
        return self._xmin

    @xmin.setter
    def xmin(self, val):
        self._xmin = val
        self.xres = abs(self._xmax - self.xmin) + 1
        return

    @property
    def xmax(self):
        return self._xmax

    @xmax.setter
    def xmax(self, val):
        self._xmax = val
        self.xres = abs(self._xmax - self.xmin) + 1
        return

    @property
    def ymin(self):
        return self._ymin

    @ymin.setter
    def ymin(self, val):
        self._ymin = val
        self.yres = abs(self._ymax - self.ymin) + 1
        return

    @property
    def ymax(self):
        return self._ymax

    @ymax.setter
    def ymax(self, val):
        self._ymax = val
        self.yres = abs(self._ymax - self.ymin) + 1
        return


    def __keytransform__(self, key):
        return key

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            print("Cannot add key:", key)
            return
        if not isinstance(value, GameTile):
            print("Cannot add key-value pair:", key, value)
            return
        if key[0] < self.xmin:
            self.xmin = key[0]
        if key[0] > self.xmax:
            self.xmax = key[0]
        if key[1] < self.ymin:
            self.ymin = key[1]
        if key[1] > self.ymax:
            self.ymax = key[1]
        return dict.__setitem__(self, self.__keytransform__(key), value)

    def render(self):
        img = Image.new('RGB', (self.xres * PIXELSCALE, self.yres * PIXELSCALE), self.backgroundcolor)
        pixels = img.load()

        for key in self.keys():
            for i in range(PIXELSCALE):
                for j in range(PIXELSCALE):
                    pixels[key[0] * PIXELSCALE + i, key[1] * PIXELSCALE + j] = self[key].color

        #img.show()
        return img



def part1():
    ICC = IntCodeComputer(threaded=False)
    MyScreen = Screen()

    ICC.loadProgram(brickbreaker)
    ICC.run()

    blockcount = 0

    while len(ICC.outputs) >= 3:
        pixelx = ICC.readOutput()
        pixely = ICC.readOutput()
        pixeltype = ICC.readOutput()
        MyScreen[(pixelx, pixely)] = GameTile(tileid=pixeltype)
        if pixeltype == 2:
            blockcount += 1

    img = MyScreen.render()
    img.save("part1.png")
    print("Number of block tiles:", blockcount)


#part1()

def part2():
    ICC = IntCodeComputer(threaded=True)
    MyScreen = Screen()
    brickbreaker[0] = 2

    highscore = -1
    blockscore = float('inf')

    ICC.loadProgram(brickbreaker)

    ICC.run()

    inputsequence = []

    score = 0
    blockcount = 0

    frame = 0
    paddlex = 0
    ballx = 0

    while ICC.running:
        if len(inputsequence):
            ICC.loadInputs([inputsequence.pop(0)])
        #else:
        #    inputsequence.append(random.randint(-1, 1))


        while len(ICC.outputs) >= 3:
            pixelx = ICC.readOutput()
            pixely = ICC.readOutput()
            pixeltype = ICC.readOutput()
            if int(pixeltype) == 3:
                paddlex = pixelx
            if int(pixeltype) == 4:
                ballx = pixelx
                if ballx > paddlex:
                    inputsequence.append(1)
                elif ballx < paddlex:
                    inputsequence.append(-1)
                else:
                    inputsequence.append(0)
                print(ballx, paddlex)

            if int(pixelx) == -1 and int(pixely) == 0:
                score = int(pixeltype)
            else:
                MyScreen[(pixelx, pixely)] = GameTile(tileid=pixeltype)

        try:
            img = MyScreen.render()
            img.save("part2_" + str(frame) + ".png")
            frame += 1
        except:
            continue

    for pixel in MyScreen.keys():
        if MyScreen[pixel].tileid == 2:
            blockcount += 1

    if score > highscore or blockcount < blockscore:
        print("Score:", score, ", Blocks:", blockcount, ICC.inputlog)
        highscore = score
        blockscore = blockcount
    #time.sleep(1)

part2()