#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import chardet
import time
import itertools
from subprocess import Popen, PIPE


yubikeyPersonalize = 'bin/ykpersonalize.exe'
ykProfile = '-2'    # choose second profile
ykKey = '-c' + '001122'    # 6 bytes hex 00 11 22 33 44 55
ykPrompt = '-y'     # always commit
pRange = 6


if pRange == 6:
    bruteKeys = [0,0,0,0,0,0, 1,1,1,1,1,1, 2,2,2,2,2,2, 3,3,3,3,3,3, 4,4,4,4,4,4, 5,5,5,5,5,5, 6,6,6,6,6,6, 7,7,7,7,7,7, 8,8,8,8,8,8, 9,9,9,9,9,9]

if pRange == 5:
    bruteKeys = [0,0,0,0,0, 1,1,1,1,1, 2,2,2,2,2, 3,3,3,3,3, 4,4,4,4,4, 5,5,5,5,5, 6,6,6,6,6, 7,7,7,7,7, 8,8,8,8,8, 9,9,9,9,9]

if pRange == 4:
    bruteKeys = [0,0,0,0, 1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7,7, 8,8,8,8, 9,9,9,9]

if pRange == 3:
    bruteKeys = [0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9]

if pRange == 2:
    bruteKeys = [0,0, 1,1, 2,2, 3,3, 4,4, 5,5, 6,6, 7,7, 8,8, 9,9]
else:
    bruteKeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


totalKeys = 16**6
totalKeysKnown = 16**4
totalKeyGuesses = totalKeys - totalKeysKnown

timeStart = time.time()

#print(totalKeys, 'total possibilities (6 bytes hex key)')
#print(totalKeysKnown, 'total known possibilities (4 bytes hex key)')
#print('Key guesses required: ', totalKeyGuesses, sep='')


#  for a in itertools.permutations([8,8,8,8,0,0,0,0], r=4): print(a[0], a[1], a[2], a[3], sep='')
#  for a in itertools.permutations(range(0, 10), r=4): print(a[0], a[1], a[2], a[3], sep='')


def unique(iterable):
    seen = set()
    for x in iterable:
        if x in seen:
            continue
        seen.add(x)
        yield x


totalKeys = 0
for a in unique(itertools.permutations(bruteKeys, r=pRange)):
#for a in itertools.permutations(bruteKeys, r=pRange):
    totalKeys = totalKeys + 1
    bruteKeysCount = totalKeys

for a in unique(itertools.permutations(bruteKeys, r=pRange)):
#for a in itertools.permutations(bruteKeys, r=pRange):
    bruteKeysCount = bruteKeysCount - 1


    if pRange == 6:
        key1, key2, key3, key4, key5, key6 = a      # convert tuple to int
        ykKeyGuess = ykKey + str(key1) + str(key2) + str(key3) + str(key4) + str(key5) + str(key6)
    if pRange == 5:
        key1, key2, key3, key4, key5 = a
        ykKeyGuess = ykKey + str(key1) + str(key2) + str(key3) + str(key4) + str(key5)
    if pRange == 4:
        key1, key2, key3, key4 = a
        ykKeyGuess = ykKey + str(key1) + str(key2) + str(key3) + str(key4)
    if pRange == 3:
        key1, key2, key3 = a
        ykKeyGuess = ykKey + str(key1) + str(key2) + str(key3) + str('0')
    if pRange == 2:
        key1, key2 = a
        ykKeyGuess = ykKey + str(key1) + str(key2) + str('0') + str('0')


    #call([yubikeyPersonalize, ykProfile, ykKeyGuess, ykPrompt, '-z'])

    p = Popen([yubikeyPersonalize, ykProfile, ykKeyGuess, ykPrompt, '-z'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode

    errEncoding = chardet.detect(err)
    keyFail = re.findall('Yubikey core error: write error', err.decode(errEncoding['encoding']))
    ykExcept1 = re.findall('Invalid access code string:', err.decode(errEncoding['encoding']))

    if not keyFail \
            and not ykExcept1:
        print('Key Found! ', ykKey[2:10], sep='')
        break
    else:
        print('incorrect key:', ykKeyGuess[2:], '...', 'keys remaining:', bruteKeysCount)

        #if ykKeyGuess[10:] == 1111:
        #    break

        if bruteKeysCount is 0:
            timeEnd = time.time()
            print('\n')
            print('Out of', totalKeys, 'keys, none worked')
            print('\n')

            if round((timeEnd - timeStart) / 60) == 0:
                print('Last run took:', timeEnd - timeStart, 'seconds')
            elif (timeEnd - timeStart) / 60 < 60:
                print('Last run took:', (timeEnd - timeStart) / 60, 'minutes')
            elif (timeEnd - timeStart) / 60 > 60:
                print('Last run took:', (timeEnd - timeStart) / 60 / 60, 'hours')
