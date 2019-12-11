# --- Day 6: Universal Orbit Map ---
#
#   Part 1: Build tree of objects orbiting one another
#   Part 2: Find number of jumps between orbits from YOU to SANta
#


f = open("input.txt", 'r')
txt = f.read()
f.close()

# txt = """
# B)G
# E)J
# J)K
# D)E
# C)D
#
# E)F
#
# G)H
# D)I
# COM)B
# B)C
#
#
# K)L
# """

lines = txt.split('\n')

class DepthVariable():
    def __init__(self):
        self._value = 0
        self._callbacks = []

    def setValue(self, value):
        self.value = value + 1

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for callback in self._callbacks:
            callback(value)

    @value.getter
    def value(self):
        return self._value

    def bind_to(self, callback):
        self._callbacks.append(callback)


class Orbiter():
    def __init__(self, name):
        self.name = name
        self._parent = None
        self.depth = DepthVariable()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

        self._parent.depth.bind_to(self.depth.setValue)


Tree = {}

for line in lines:
    if len(line):
        parent = line.split(")")[0]
        child = line.split(")")[1]
        if parent not in Tree.keys():
            Tree[parent] = Orbiter(parent)
        if child not in Tree.keys():
            Tree[child] = Orbiter(child)
        Tree[child].parent = Tree[parent]
        Tree[child].depth.value = Tree[parent].depth.value + 1



orbits = 0
for key in Tree.keys():
    #print(key, Tree[key].depth.value)
    orbits += Tree[key].depth.value

print(orbits)

YOUparents = []
activeNode = Tree["YOU"]
while activeNode != Tree["COM"]:
    YOUparents.append(activeNode.parent)
    activeNode = activeNode.parent


SANparents = []
activeNode = Tree["SAN"]
while activeNode != Tree["COM"]:
    SANparents.append(activeNode.parent)
    activeNode = activeNode.parent

maxDepth = 0
commonNode = Tree["COM"]
for node in YOUparents:
    if node in SANparents:
        if node.depth.value > maxDepth:
            commonNode = node
            maxDepth = commonNode.depth.value

print(Tree["YOU"].depth.value)
print(YOUparents)
print(Tree["SAN"].depth.value)
print(SANparents)
print(commonNode.depth.value)

print("Answer: ", Tree["SAN"].depth.value - commonNode.depth.value + Tree["YOU"].depth.value - commonNode.depth.value - 2)