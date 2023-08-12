# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import time
import math
from smbus2 import SMBus


SMBUS_INTERFACE = 3

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04


logger = logging.getLogger(__name__)

class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, interface=SMBUS_INTERFACE, address=PCA9685_ADDRESS):
        """
        Initialize the PCA9685 chip at the provided address on the specified I2C bus number.
        The default address is 0x40 and the default bus is 3.

        Args:
            interface (int): The I2C bus number to use (default 3)
            address (int): The I2C address of the PCA9685 chip (default 0x40)
        """
        self.interface = interface
        self.address = address

        self.set_all_pwm(0, 0)
        with SMBus(self.interface) as bus:
            bus.write_byte_data(self.address, MODE2, OUTDRV)
            bus.write_byte_data(self.address, MODE1, ALLCALL)
            time.sleep(0.005) # wait for oscillator
            mode1 = bus.read_byte_data(self.address, MODE1)
            mode1 = mode1 & ~SLEEP # wake up (reset sleep)
            bus.write_byte_data(self.address, MODE1, mode1)
            time.sleep(0.005) # wait for oscillator

    def set_pwm_freq(self, freq_hz):
            """
            Sets the PWM frequency of the PCA9685 module.

            Args:
                freq_hz (float): The desired frequency in Hz. Valid from 24 Hz to 1526 Hz.
            """
            prescaleval = 25000000.0    # 25MHz
            prescaleval /= 4096.0       # 12-bit
            prescaleval /= float(freq_hz)
            prescaleval -= 1.0
            logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
            logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
            prescale = int(math.floor(prescaleval + 0.5))
            logger.debug('Final pre-scale: {0}'.format(prescale))
            with SMBus(self.interface) as bus:
                oldmode = bus.read_byte_data(self.address, MODE1)
                newmode = (oldmode & 0x7F) | 0x10    # sleep
                bus.write_byte_data(self.address, MODE1, newmode)  # go to sleep
                bus.write_byte_data(self.address, PRESCALE, prescale)
                bus.write_byte_data(self.address, MODE1, oldmode)
                time.sleep(0.005)
                bus.write_byte_data(self.address, MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
            """
            Sets the on and off time for a specific channel on the PCA9685 PWM controller.
            
            Args:
                channel (int): The channel number to set the on and off time for.
                on (int): The value for the on time of the PWM signal.
                off (int): The value for the off time of the PWM signal.
            """
            with SMBus(self.interface) as bus:
                bus.write_byte_data(self.address, LED0_ON_L+4*channel, on & 0xFF)
                bus.write_byte_data(self.address, LED0_ON_H+4*channel, on >> 8)
                bus.write_byte_data(self.address, LED0_OFF_L+4*channel, off & 0xFF)
                bus.write_byte_data(self.address, LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
            """
            Sets the on and off values for all channels of the PCA9685 PWM controller.
            
            Args:
                on (int): The value to set the on time for all channels.
                off (int): The value to set the off time for all channels.
            """
            with SMBus(self.interface) as bus:
                bus.write_byte_data(self.address, ALL_LED_ON_L, on & 0xFF)
                bus.write_byte_data(self.address, ALL_LED_ON_H, on >> 8)
                bus.write_byte_data(self.address, ALL_LED_OFF_L, off & 0xFF)
                bus.write_byte_data(self.address, ALL_LED_OFF_H, off >> 8)

    def software_reset(self):
        """Sends a software reset (SWRST) command to all servo drivers on the bus."""
        #self._device.writeRaw8(0x06)
        with SMBus(self.interface) as bus:
            bus.write_byte_data(self.address, 0x06, 0x00)