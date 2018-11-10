#!/usr/bin/env python3
# -*- coding: utf8 -*-


import re
import os
import sys
import time
import random
import chardet
import asyncio
import logging
import platform
import itertools

from subprocess import Popen, PIPE

logging.basicConfig(level=logging.FATAL)


class Yubikey:
    """ wrapper for ykpersonalize
    """

    def __init__(self, dev=None):
        self.device = dev

        self.YK_PROFILE_ARG = '-2'  # choose second profile
        self.YK_KEY_ARG = '-c'  # 6 bytes hex 00 11 22 33 44 55
        self.YK_PROMPT_ARG = '-y'  # always commit
        self.YK_DELETE_ARG = '-z'  # delete the configuration in slot 1 or 2
        self.ARRAY_RANGE = 12

        self.KNOWN = ''

        self.YUBIKEY_PERSONALIZE = {
            'Windows': os.path.join('win', 'bin', 'ykpersonalize.exe'),
            'Linux': os.path.join('linux', 'ykpers-1.18.0', 'ykpersonalize')
        }

        try:
            self.YUBIKEY_PERSONALIZE = self.YUBIKEY_PERSONALIZE[platform.system()]
        except:
            Exception('OS not supported')
            sys.exit(1)

    async def _run(self, key):
        """ run ykpersonalize
        """
        YK_KEY_GUESS = self.KNOWN + key
        cmd = [self.YUBIKEY_PERSONALIZE, self.YK_PROFILE_ARG, self.YK_PROMPT_ARG, self.YK_DELETE_ARG, YK_KEY_GUESS]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        # rc = p.returncode

        err_encoding = chardet.detect(error)
        KEY_FAIL = [
            re.findall('Yubikey core error: write error', error.decode(err_encoding['encoding'])),
            re.findall('Invalid access code string:', error.decode(err_encoding['encoding']))
        ]

        FAILED = 0

        for check in KEY_FAIL:
            if check:
                FAILED += 1

        if FAILED == 0:
            # print('Key Found! ', YK_KEY_GUESS[2:10], sep='')
            print('Key Found! {}'.format(YK_KEY_GUESS))
            sys.exit(0)
        else:
            print('.', end='')
            sys.stdout.flush()
            logging.error('incorrect key: {}'.format(YK_KEY_GUESS))

    def _key_gen(self, limit=None):
        """ generate keys
        """
        i = 0
        for a in itertools.product(range(10), repeat=self.ARRAY_RANGE):
            if limit:
                if i < limit:
                    yield ''.join(list(str(x) for x in a))
                i += 1
            else:
                yield ''.join(list(str(x) for x in a))

    async def show_keys(self, limit=None):
        """ show generated keys
        """
        for a in self._key_gen(limit):
            print(self.KNOWN + a)

    def input_key(self):
        """ lets user input key
        """
        a = str(input('Type in known: '))
        self.ARRAY_RANGE = 12
        self.set_secret(a)

    def set_secret(self, input_key=None):
        """ set key
        """
        assert type(input_key) is str
        assert int(input_key)
        assert len(input_key) <= self.ARRAY_RANGE
        if input_key:
            self.ARRAY_RANGE -= len(input_key)
        self.KNOWN = input_key
        logging.info('known key digits: {}'.format(len(input_key)))
        logging.info('unknown key digits: {}'.format(self.ARRAY_RANGE))

    async def test_key(self, test_key):
        await self._run(self.set_secret(test_key))

    async def find_my_key(self):
        """ start brute forcing
        """
        start_time = int(time.time())
        total_keys = 10 ** self.ARRAY_RANGE
        tries = total_keys
        print('total unknown keys: {}'.format(total_keys))
        for a in self._key_gen():
            await self._run(a)
            if random.choice(range(100)) == 3:
                print('{} tries left'.format(total_keys), end='')
            total_keys -= 1

        end_time = time.time()
        print('\n')
        print('Out of', tries, 'keys, none worked')
        print('\n')

        if round((end_time - start_time) / 60) == 0:
            print('That run took:', round(end_time - start_time), 'seconds')
        elif (end_time - start_time) / 60 < 60:
            print('That run took:', round(end_time - start_time) / 60, 'minutes')
        elif (end_time - start_time) / 60 > 60:
            print('That run took:', (end_time - start_time) / 60 / 60, 'hours')


async def main():
    y = Yubikey()
    y.input_key()
    await y.find_my_key()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
