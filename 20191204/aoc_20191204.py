import time

starttime = time.time()

possibilities = [str(num) for num in range(156218,652527)]

valid = []

for password in possibilities:
    if "11" in password \
    or "22" in password \
    or "33" in password \
    or "44" in password \
    or "55" in password \
    or "66" in password \
    or "77" in password \
    or "88" in password \
    or "99" in password:
        if int(password[0]) <= int(password[1]) \
        and int(password[1]) <= int(password[2]) \
        and int(password[2]) <= int(password[3]) \
        and int(password[3]) <= int(password[4]) \
        and int(password[4]) <= int(password[5]):
            valid.append(password)

print(valid)
print(len(valid))

valid2 = []

for password in valid:
    repeats = {}
    for i in range(5):
        if int(password[i]) == int(password[i+1]):
            if password[i] in repeats.keys():
                repeats[password[i]] += 1
            else:
                repeats[password[i]] = 2
    allEven = True
    for value in repeats.values():
        if value > 2:
            allEven = False
    if 2 in repeats.values():
        allEven = True

    if allEven:
        valid2.append(password)

print(valid2)
print(len(valid2))

print(time.time() - starttime)