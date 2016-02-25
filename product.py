#!/usr/bin/env python
# -*- coding: utf8 -*-

import itertools
import re


regex = '090'
start = 0

for tuples in itertools.product(range(10), repeat=4):
    try:
        #a,b,c,d,e,f,g,h,i,j,k,l = tuples
        #print(a,b,c,d,e,f,g,h,i,j,k,l, sep='')
        #print(a,b,c, sep='')
        start += 1

    finally:
        None

print(start)