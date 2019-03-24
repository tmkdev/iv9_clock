import datetime
import time
import logging
import os

from shiftregister import ShiftRegister
from mapping import *

def replace_zero(datestring):
    if datestring.startswith('0'):
        datestring = datestring.replace('0', ' ', 1)
    return datestring

def get_twotube():
    now = datetime.datetime.now()
    if now.second % 2:
        return replace_zero(now.strftime('%H')), True
    else:
        return now.strftime('%M'), False

def get_fourtube():
    now = datetime.datetime.now()
    ispm = False if now.strftime('%p') == 'PM' else True

    return replace_zero(now.strftime('%H%M')), ispm

def clock(numtubes=2):
    shiftreg = ShiftRegister(num_registers=numtubes)
    while True:
        if numtubes == 2:
            chars, ishour = get_twotube()
        elif numtubes == 4:
            chars, ispm = get_fourtube()

        print(chars)
        bytelist = []

        for c in chars:
            char = segment_map[str(c)]
            bytelist.append(char)
            logging.info(str_rep(char))

        #Map Periods. 
        if numtubes == 2 and ishour:
            bytelist[0] = bytelist[0] | 0x80
        else:
            bytelist[1] = bytelist[1] | 0x80

        if numtubes == 4 and ispm:
            bytelist[1] = bytelist[1] | 0x80
        else:
            bytelist[2] = bytelist[2] | 0x80

        shiftreg.write(bytelist)

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        numtubes = int(os.getenv('NUMTUBES', '2'))
    except:
        logging.critical('Please set NUMTUBES env - 2 or 4 supported.')
    logging.warning('Starting clock with {0} tubes'.format(numtubes))

    clock(numtubes)
