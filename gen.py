# -*- coding: utf-8 -*-
import io
import os
import random
import re
import string
import sys
from typing import TextIO


RANGES = {
    r'[A-ZА-ЯЁ]': lambda _: random.choice(string.ascii_uppercase),
    r'[a-zа-яё]': lambda _: random.choice(string.ascii_lowercase),
    r'\d': lambda _: random.choice(string.digits)
}


class Randomizer:
    def __init__(self, stream: TextIO, line_sep: string=os.linesep, col_sep: string='\t'):
        self.__cache = {}
        self.__stream = stream
        self.__col_sep = col_sep
        self.__line_sep = line_sep

    def get_randomized(self) -> string:
        return self.__line_sep.join([self._randomize_line(line.rstrip(self.__line_sep)) for line in self.__stream]

    def _randomize_line(self, line: string) -> string:
        return self.__col_sep.join([self._randomize_col(col) for col in line.split(self.__col_sep)])
    def _randomize_col(self, col: string) -> string:
        randomized_col = self.__cache.get(col)

        if randomized_col is None:
            randomized_col = col

            for regexp in RANGES:
                randomized_col = re.sub(regexp, RANGES[regexp], randomized_col)

            self.__cache[col] = randomized_col

        return randomized_col


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1].strip()) as f:
            result = Randomizer(f).get_randomized()
    else:
        result = Randomizer(sys.stdin).get_randomized()

    print(result)
