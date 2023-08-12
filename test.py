from PCA9685.PCA9685 import PCA9685
import time


pwm = PCA9685() # use default I2C bus 3, default address 0x40
pwm.set_pwm_freq(50) # set frequency to 50 Hz for SG90 servos

# set servo to neutral position
pwm.set_pwm(0, 0, 375) # channel 0, off = 375
time.sleep(1) # wait for servo to move

# set servo to 90 degrees
pwm.set_pwm(0, 0, 225) # channel 0, off = 225
time.sleep(1) # wait for servo to move

# set servo to 180 degrees
pwm.set_pwm(0, 0, 75) # channel 0, off = 75
time.sleep(1) # wait for servo to move