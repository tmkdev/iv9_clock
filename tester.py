import datetime
import time
import logging
import os
from itertools import cycle

from shiftregister import ShiftRegister
from mapping import *

numerals = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]


def tester():
    shiftreg = ShiftRegister(num_registers=1)
    chars = cycle(numerals)

    while True:
        bytelist = []

        char = segment_map[str(next(chars))]
        bytelist.append(char)
        logging.warning(str_rep(char))
        #shiftreg.write(bytelist)
        
        time.sleep(1)

if __name__ == '__main__':
    tester()