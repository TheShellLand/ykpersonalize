#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, itertools

regex = '8899'
search = re.compile(regex)

MATCHES = 0
NO_MATCH = 0

for LIST in itertools.product(range(10), repeat=4):
    a,b,c,d = LIST
    #print(str(LIST))
    #print(str(a) + str(b) + str(c) + str(d))
    answer = str(a) + str(b) + str(c) + str(d)
    #print(answer)

    if re.findall(regex, answer):
        print(answer)
        MATCHES += 1
    else:
        NO_MATCH += 1

print('Matches:', MATCHES)
print('No Matches:', NO_MATCH)


