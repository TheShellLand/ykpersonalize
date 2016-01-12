#!/usr/bin/env python
# -*- coding: utf8 -*-


import itertools
import os
import re


pRange = 4
#bruteKeys = [0,0,0,0, 1,1,0,0, 2,2,0,0, 3,3,0,0, 4,4,0,0, 5,5,0,0, 6,6,0,0, 7,7,0,0, 8,8,0,0, 9,9,0,0]
bruteKeys = [0,0,0,0, 1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7,7, 8,8,8,8, 9,9,9,9]
#bruteKeys = [1,2,3,4,5,6,7,8,9]
#bruteKeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

#bruteKeys = range(0, 10)
regex = '8, 9, 0, 0'

fComb = 'combinations-combinations.list'
fPerm = 'combinations-permutations.list'


def unique(iterable):
    seen = set()
    for x in iterable:
        if x in seen:
            continue
        seen.add(x)
        yield x


if not os.path.isfile(fComb):
    totalKeys = 0
    with open(fComb, 'w') as f:
        for a in unique(itertools.combinations(bruteKeys, r=pRange)):
            if re.search('(.,)', str(a)):
                re.sub('[,()]', '', str(a))
            totalKeys = totalKeys + 1
            f.write(str(a))
    f.close()

if not os.path.isfile(fPerm):
    totalKeys = 0
    with open(fPerm, 'w') as f:
        for a in unique(itertools.permutations(bruteKeys, r=pRange)):
            if re.search('(.,)', str(a)):
                re.sub('[,()]', '', str(a))
            totalKeys = totalKeys + 1
            f.write(str(a))
    f.close()

# Search
with open(fComb, 'r') as f:
    count = len(re.findall(regex, f.read()))
    print(fComb, 'Regex:', regex, 'Count:', count)

with open(fPerm, 'r') as f:
    count = len(re.findall(regex, f.read()))
    print(fPerm, 'Regex:', regex, 'Count:', count)

# Total
with open(fComb, 'r') as f:
    regex = '., ., ., .'
    count = len(re.findall(regex, f.read()))
    print(fComb, 'Regex:', regex, 'Count:', count)

with open(fPerm, 'r') as f:
    regex = '., ., ., .'
    count = len(re.findall(regex, f.read()))
    print(fPerm, 'Regex:', regex, 'Count:', count)

