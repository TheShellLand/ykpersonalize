#!/usr/bin/env python3
# -*- coding: utf8 -*-


import re
import chardet
import time
import itertools
import platform
from subprocess import Popen, PIPE

YUBIKEY_PERSONALIZE_WIN = 'win/bin/ykpersonalize.exe'
YUBIKEY_PERSONALIZE_LINUX = 'linux/ykpers-1.18.0/ykpersonalize'
YK_PROFILE = '-2'  # choose second profile
YK_KEY = '-c'  # 6 bytes hex 00 11 22 33 44 55
YK_PROMPT = '-y'  # always commit
ARRAY_RANGE = 12

if platform.system() == 'Linux':
    YUBIKEY_PERSONALIZE = YUBIKEY_PERSONALIZE_LINUX
else:
    YUBIKEY_PERSONALIZE = YUBIKEY_PERSONALIZE_WIN


KNOWN = input('Type in known: ')
if KNOWN:
    ARRAY_RANGE -= len(KNOWN)

TOTAL_KEYS = 10 ** ARRAY_RANGE

TIME_START = time.time()

for a in itertools.product(range(10), repeat=ARRAY_RANGE):

    TOTAL_KEYS -= 1

    # convert tuple to int
    if ARRAY_RANGE == 12:
        # key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11, key12 = a
        key12, key11, key10, key9, key8, key7, key6, key5, key4, key3, key2, key1 = a
        YK_KEY_GUESS = YK_KEY + str(key1) + str(key2) + str(key3) + str(key4) + str(key5) + str(key6) + str(key7) + str(
            key8) + str(key9) + str(key10) + str(key11) + str(key12)

    elif ARRAY_RANGE == 4:
        # key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11, key12 = a
        key4, key3, key2, key1 = a
        YK_KEY_GUESS = YK_KEY + KNOWN + str(key1) + str(key2) + str(key3) + str(key4)

    # call([YUBIKEY_PERSONALIZE, YK_PROFILE, YK_KEY_GUESS, YK_PROMPT, '-z'])

    p = Popen([YUBIKEY_PERSONALIZE, YK_PROFILE, YK_KEY_GUESS, YK_PROMPT, '-z'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode

    err_encoding = chardet.detect(err)
    KEY_FAIL = re.findall('Yubikey core error: write error', err.decode(err_encoding['encoding']))
    YK_EXCEPT_1 = re.findall('Invalid access code string:', err.decode(err_encoding['encoding']))

    if not KEY_FAIL \
            and not YK_EXCEPT_1:
        # print('Key Found! ', YK_KEY_GUESS[2:10], sep='')
        print('Key Found! ', YK_KEY_GUESS[2:], sep='')
        break

    else:
        print('incorrect key:', YK_KEY_GUESS[2:], '...', 'keys remaining:', TOTAL_KEYS)

        if TOTAL_KEYS is 0:
            TIME_END = time.time()
            print('\n')
            print('Out of', TOTAL_KEYS, 'keys, none worked')
            print('\n')

            if round((TIME_END - TIME_START) / 60) == 0:
                print('Last run took:', TIME_END - TIME_START, 'seconds')
            elif (TIME_END - TIME_START) / 60 < 60:
                print('Last run took:', (TIME_END - TIME_START) / 60, 'minutes')
            elif (TIME_END - TIME_START) / 60 > 60:
                print('Last run took:', (TIME_END - TIME_START) / 60 / 60, 'hours')

print('End')
