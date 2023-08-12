# Python-PCA9685

A ~~probably~~ definitely not-best-practices way to use the PCA9685 with an Orange Pi Zero 3.

If it works, it works.

## Purpose

This library replaces [adafruit/Adafruit_Python_PCA9685](https://github.com/adafruit/Adafruit_Python_PCA9685) for
the Orange Pi Zero 3 and presumably other single board computers that may or may not have reliable Blinka support.

## Usage

This will set an SG90 micro servo plugged into channel 0 to spin to the -90° position.

```python
from PCA9685_smbus2 import PCA9685

pwm = PCA9685.PCA9685() # defaults to using i2c-3 and address 0x40
pwm.set_pwm_freq(50) # set frequency to 50 Hz for SG90 servos

pwm.set_pwm(0, 0, 102) # channel 0, on time 0?, off time 102 (1 ms)
```

The `on` and `off` times above are the number of ticks on the PCA9685, which has a 12-bit resolution and therefore can range from 0 to 4096.

## Tested on

This library has been tested on:
- Orange Pi Zero 3

It likely supports any board in which the accessible I2C bus can be found by running `ls /dev/i2c-*`, since it relies on the [smbus2](https://github.com/kplindegaard/smbus2) library for I2C interfacing.

Ensure that the relevant I2C interface has been enabled in `sudo orangepi-config` or `sudo raspi-config` (or whatever the case may be) for this to work right.