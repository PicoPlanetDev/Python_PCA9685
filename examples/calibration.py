from PCA9685_smbus2 import PCA9685
import time


pwm = PCA9685.PCA9685() # use default I2C bus 3, default address 0x40
pwm.set_pwm_freq(50) # set frequency to 50 Hz for SG90 servos

print("Press Ctrl+C to quit...")
while True:
    off_time = int(input("Enter off time: "))
    pwm.set_pwm(0, 0, off_time) # channel 0, off time 102 (1 ms)
    print(f"Setting servo with off time {off_time}")
    time.sleep(1)