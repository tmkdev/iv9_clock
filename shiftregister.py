#https://learn.pimoroni.com/tutorial/170pt-projects/the-shift-register-170pt
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)


class ShiftRegister(object):
    def __init__(self, data_pin=22, latch_pin=27, clock_pin=17, num_registers=1):
        self.PIN_DATA = data_pin
        self.PIN_LATCH = latch_pin
        self.PIN_CLOCK = clock_pin
        self.num_registers = num_registers

        self.current_data = None

        logging.info('Data Pin: {0} Latch Pin: {1} Clock Pin: {2}'.format(self.PIN_DATA, self.PIN_LATCH, self.PIN_CLOCK))

        self.setup()

    def setup(self):
        GPIO.setup(self.PIN_DATA,  GPIO.OUT)
        GPIO.setup(self.PIN_LATCH, GPIO.OUT)
        GPIO.setup(self.PIN_CLOCK, GPIO.OUT)

        logging.info('GPIO Set up')


    def get_current(self):
        return self.current_data

    def write(self, byte_array):
        byte_array = byte_array[0:self.num_registers]

        self.current_data = byte_array

        self._unlatch()
        for byte in byte_array:
            self._shiftout(byte)
        self._latch()

        return len(byte_array)

    def _unlatch(self):
        GPIO.output(self.PIN_LATCH, 0)
    
    def _latch():
         GPIO.output(self.PIN_LATCH, 1)

    def _shiftout(byte):
        for x in range(8):
            GPIO.output(self.PIN_DATA, (byte >> x) & 1)
            GPIO.output(self.PIN_CLOCK, 1)
            GPIO.output(self.IN_CLOCK, 0)


