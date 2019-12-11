# --- Day 4: Secure Container ---
#
#   Part 1: Find number of possible 6-digit passwords given restrictions
#   Part 2: Shortest distance along wires (combined) to reach the first intersection
#

import time

starttime = time.time()

possibilities = [str(num) for num in range(156218,652527)]
validPasswords = []

for password in possibilities:
    for pair in ["11", "22", "33", "44", "55", "66", "77", "88", "99"]:
        if pair in password:
            monotonic = True
            for i in range(5):
                if int(password[i]) > int(password[i+1]):
                    monotonic = False
                    break
            if monotonic:
                validPasswords.append(password)
                break
            else:
                break

print(len(validPasswords))
# 1694

validPasswords2 = []

for password in validPasswords:
    repeats = {}
    for i in range(5):
        if int(password[i]) == int(password[i+1]):
            if password[i] in repeats.keys():
                repeats[password[i]] += 1
            else:
                repeats[password[i]] = 2
    stillValid = True
    for value in repeats.values():
        if value > 2:
            stillValid = False
    if 2 in repeats.values():
        stillValid = True

    if stillValid:
        validPasswords2.append(password)

print(len(validPasswords2))
# 1148

print(time.time() - starttime)