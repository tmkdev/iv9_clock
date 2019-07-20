import argparse
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

def get_fourtube(miltime):
    now = datetime.datetime.now()
    ispm = False if now.strftime('%p') == 'PM' else True

    if miltime:
        return replace_zero(now.strftime('%H%M')), ispm
        
    return replace_zero(now.strftime('%I%M')), ispm

def clock(args):
    shiftreg = ShiftRegister(num_registers=numtubes)
    ishour = False
    ispm = False

    while True:
        if args.numtubes == 2:
            chars, ishour = get_twotube()
        elif args.numtubes == 4:
            chars, ispm = get_fourtube(args.miltime)

        bytelist = []

        #Reverse the order of the string - clocks into the clock backwards.
        for c in chars[::-1]:
            char = segment_map[str(c)]
            bytelist.append(char)
            logging.info(str_rep(char))

        #Map Periods.
        if numtubes == 2:
            if ishour:
                bytelist[1] = bytelist[1] | 0x80
            else:
                bytelist[0] = bytelist[0] | 0x80

        if numtubes == 4:
            if args.ampm 
                if ispm:
                    bytelist[2] = bytelist[2] | 0x80
                else:
                    bytelist[3] = bytelist[3] | 0x80

            if args.seconds and datetime.datetime.now().second % 2:
                bytelist[1] = bytelist[1] | 0x80

        shiftreg.write(bytelist)

        time.sleep(0.1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Numitron Clock')
    parser.add_argument('--numtubes', action='store', type=int, default=4, help='Number of numitron tube supported. Defaults to 4.')
    parser.add_argument('--ampm', action='store', type=bool, default=False, help='AmPm indicator enable. Defaults false.')
    parser.add_argument('--seconds', action='store', type=bool, default=False, help='Flashing Seconds indicator. Defaults false.')
    parser.add_argument('--miltime', action='store', type=bool, default=False, help='24 Hour display. Defaults to False. (12H)')

    args = parser.parse_args()

    clock(args)
