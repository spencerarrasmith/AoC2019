IMAGEX = 25
IMAGEY = 6

f = open('input.txt', 'r')
txt = f.read().lstrip().rstrip()
f.close()

# IMAGEX = 3
# IMAGEY = 2
# txt = "123456789012"

img = []
layer = -1
p=0
while p < len(txt):
    img.append([])  # New layer
    layer += 1
    for i in range(IMAGEY):
        img[layer].append(txt[p:p+IMAGEX])
        p+=IMAGEX

zerocounts = [0 for x in range(len(img))]
for i,layer in enumerate(img):
    for row in layer:
        zerocounts[i] += row.count("0")

#print(min(zerocounts), " on layer ", zerocounts.index(min(zerocounts)))

ones = 0
twos = 0
for i,row in enumerate(img[zerocounts.index(min(zerocounts))]):
    ones += row.count('1')
    twos += row.count('2')

#print(ones, twos, ones*twos)

collapsedimage = [['2' for i in range(IMAGEX)] for j in range(IMAGEY)]

img.reverse()

for layer in img:
    for i,row in enumerate(layer):
        for j,column in enumerate(row):
            if layer[i][j] != '2':
                collapsedimage[i][j] = layer[i][j]

for row in collapsedimage:
    print(row)