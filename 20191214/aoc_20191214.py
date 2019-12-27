f = open("input.txt", 'r')
mainrecipe = f.read().strip().split('\n')
f.close()

recipe1 = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""".strip().split('\n')


def part1(recipe):
    costs = {}
    surplus = {}
    for line in recipe:
        l = line.split("=>")
        costs[l[1].strip().split(" ")[1]] = 0
        surplus[l[1].strip().split(" ")[1]] = 0


    surplus["FUEL"] = 1
    print(surplus)

    running = True
    while running:



part1(recipe1)