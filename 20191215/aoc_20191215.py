# --- Day 15: Oxygen System ---
#
#   Part 1:
#   Part 2:
#

import sys
sys.path.append("..")

import random, time, threading
from PIL import Image

import tkinter as tk
import tkinter.filedialog
from tkinter import Tk


from AoCCommon.IntCodeComputer import IntCodeComputer

PIXELSCALE = 10




class AOCWindow(tk.Frame):
    def __init__(self):
        self.root = Tk()

        self.frame = super()
        self.frame.__init__(self.root, bg='black', relief=tk.RAISED, borderwidth=4)

        self.root.geometry('1280x720+0+0')
        self.root.resizable(False, False)
        self.grid()

        self.textbox = tk.Text(self, height=44, width=158, background='black', foreground='white')
        self.textbox.grid(row=0, column=0)
        #self.textbox.configure(state="disabled")

        self.text = ["".join([" " for i in range(158)]) for j in range(44)]
        self.textbox.insert(tk.CURRENT, "\n".join(self.text))

        self.cursorline = 22
        self.cursorcolumn = 79
        self.moveCursor(self.cursorline, self.cursorcolumn)
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, "☺")

        self.root.bind("<Key-Up>", self.moveUp)
        self.root.bind("<Key-Down>", self.moveDown)
        self.root.bind("<Key-Right>", self.moveRight)
        self.root.bind("<Key-Left>", self.moveLeft)

        f = open("input.txt", 'r')
        mainprogram = f.read().split(',')
        f.close()

        self.droid = IntCodeComputer(threaded=True)
        self.droid.loadProgram(mainprogram)
        self.droid.run()
        self.rxthread = None
        self.alive = threading.Event()
        self.start_rx_thread()
        self.move_prev = 0


    def start_rx_thread(self):
        self.rxthread = threading.Thread(target=self.thread_rx)
        self.rxthread.setDaemon(1)
        self.alive.set()
        self.rxthread.start()

    def thread_rx(self):
        while self.alive.isSet():
            time.sleep(0.001)
            out = self.droid.readOutput()
            if out != None:
                print(out)
                if out == 0:
                    if self.move_prev == 1:
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "█")
                        self.cursorline += 1
                        self.moveCursor(self.cursorline, self.cursorcolumn)
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "☺")
                    if self.move_prev == 2:
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "█")
                        self.cursorline -= 1
                        self.moveCursor(self.cursorline, self.cursorcolumn)
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "☺")
                    if self.move_prev == 3:
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "█")
                        self.cursorcolumn -= 1
                        self.moveCursor(self.cursorline, self.cursorcolumn)
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "☺")
                    if self.move_prev == 4:
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "█")
                        self.cursorcolumn += 1
                        self.moveCursor(self.cursorline, self.cursorcolumn)
                        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
                        self.textbox.insert(tk.INSERT, "☺")
                elif out == 2:
                    print("ASDASHFHAHG")

    def moveCursor(self, line, column):
        self.textbox.mark_set("insert", "%d.%d" % (line + 1, column + 1))

    def moveUp(self, event=None):
        #print("Up")
        self.move_prev = 1
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, ".")
        self.cursorline -= 1
        self.moveCursor(self.cursorline, self.cursorcolumn)
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, "☺")
        self.droid.loadInputs([self.move_prev])

    def moveDown(self, event=None):
        #print("Down")
        self.move_prev = 2
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, ".")
        self.cursorline += 1
        self.moveCursor(self.cursorline, self.cursorcolumn)
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, "☺")
        self.droid.loadInputs([self.move_prev])

    def moveRight(self, event=None):
        #print("Right")
        self.move_prev = 3
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, ".")
        self.cursorcolumn += 1
        self.moveCursor(self.cursorline, self.cursorcolumn)
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, "☺")
        self.droid.loadInputs([self.move_prev])

    def moveLeft(self, event=None):
        #print("Left")
        self.move_prev = 4
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, ".")
        self.cursorcolumn -= 1
        self.moveCursor(self.cursorline, self.cursorcolumn)
        self.textbox.delete("%s-1c" % tk.INSERT, tk.INSERT)
        self.textbox.insert(tk.INSERT, "☺")
        self.droid.loadInputs([self.move_prev])

    def on_exit(self, event=None):
        self.root.destroy()



def part1():
    app = AOCWindow()
    app.root.title("Day 15")
    #app.root.iconbitmap("img/favicon_sls_32.ico")
    app.mainloop()

part1()

def part2():
    f = open("maze.txt", 'r', encoding='utf-8')
    maze = f.read()
    f.close()

    print(maze)

    print(int(1367/158), 1367 % 158)
    print(maze.split("\n")[8][103-8])
    #print(maze.find("☺"))

#part2()