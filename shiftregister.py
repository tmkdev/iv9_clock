#https://learn.pimoroni.com/tutorial/170pt-projects/the-shift-register-170pt
import logging
from time import sleep

from gpiozero.pins.mock import MockFactory
from gpiozero import Device, DigitalOutputDevice

#Todo: Make this configurable.. 
#Device.pin_factory = MockFactory()


class ShiftRegister(object):
    def __init__(self, data_pin=22, latch_pin=27, clock_pin=17, num_registers=1):
        self.data = DigitalOutputDevice(pin=data_pin)
        self.latch = DigitalOutputDevice(pin=latch_pin)
        self.clock = DigitalOutputDevice(pin=clock_pin)

        self.num_registers = num_registers

        self.current_data = None

        logging.info('Data Pin: {0} Latch Pin: {1} Clock Pin: {2}'.format(self.data.pin, self.latch.pin, self.clock.pin))

    def get_current(self):
        return self.current_data

    def write(self, byte_array):
        byte_array = byte_array[0:self.num_registers]

        if byte_array == self.current_data:
            return False

        self.current_data = byte_array

        self._unlatch()
        for byte in byte_array:
            self._shiftout(byte)
        self._latch()

        return True

    def _unlatch(self):
        self.latch.off()

    def _latch(self):
         self.latch.on()

    def _shiftout(self, byte):
        for x in range(8):
            self.data.value = (byte >> x) & 1
            self.clock.on()
            self.clock.off()

