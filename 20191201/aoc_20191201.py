# --- Day 1: The Tyranny of the Rocket Equation ---
#
#   Part 1: Fuel total for all modules in the list
#   Part 2: Fuel total for all modules and all fuel, recursively
#

import math

class ElfModule():
    def __init__(self):
        self._mass = 0
        self._fuel = 0

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        if mass >= 0:
            self._mass = mass
        else:
            self._mass = 0

    @mass.getter
    def mass(self):
        return self._mass


class FuelCounterUpper():
    def __init__(self, queue):
        print("FuelCounterUpper Online")
        self.totalFuel = 0
        self.queue = queue

    def calculateFuel(self):
        while len(self.queue):
            try:
                mass = self.queue.pop(0)
                fuel = self.fuelEquation(int(mass))
                self.totalFuel += fuel
                if fuel > 0:
                    self.queue.append(fuel)
            except:
                continue


    def fuelEquation(self, mass):
        fuel = math.floor(mass/3) - 2
        if fuel < 0:
            fuel = 0
        return fuel


f = open("input.txt", 'r')
lines = f.read()
f.close()

lines = lines.split('\n')

fuelcounter1 = FuelCounterUpper(lines)
fuelcounter1.calculateFuel()

print(fuelcounter1.totalFuel)
