from PCA9685_smbus2 import PCA9685
import time


pwm = PCA9685.PCA9685() # use default I2C bus 3, default address 0x40
pwm.set_pwm_freq(50) # set frequency to 50 Hz for SG90 servos

print("Press Ctrl+C to quit...")
while True:
    # set servo to -90 degrees
    pwm.set_pwm(0, 0, 102) # channel 0, off time 102 (1 ms)
    time.sleep(1)

    # set servo to 0 degrees
    pwm.set_pwm(0, 0, 307) # channel 0, off time 307 (1.5 ms)
    time.sleep(1)

    # set servo to 90 degrees
    pwm.set_pwm(0, 0, 512) # channel 0, off time 512 (2 ms)
    time.sleep(1)