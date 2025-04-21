import RPi.GPIO as GPIO
from time import sleep

rly_1 = 16 # IN1 on relay: blue LED
rly_2 = 20 # IN2 on relay: green LED
rly_3 = 21 # IN3 on relay: pump
rly_4 = 4 # IN4 on relay: red LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(rly_1, GPIO.OUT)
GPIO.setup(rly_2, GPIO.OUT)
GPIO.setup(rly_3, GPIO.OUT)
GPIO.setup(rly_4, GPIO.OUT)
GPIO.output(rly_1, 1)
GPIO.output(rly_2, 1)
GPIO.output(rly_3, 1)
GPIO.output(rly_4, 1)

try:
    while True:
        # print("set to 0")
        # GPIO.output(rly_1, 1)
        # GPIO.output(rly_2, 0)
        # GPIO.output(rly_3, 1)
        # sleep(20)
        # print("set to 1")
        # GPIO.output(rly_1, 0)
        # GPIO.output(rly_2, 1)
        # GPIO.output(rly_3, 0)
        # sleep(8)

        GPIO.output(rly_1, 0)
        GPIO.output(rly_3, 0)
        GPIO.output(rly_2, 1)
        GPIO.output(rly_4, 1)
        sleep(5)
        GPIO.output(rly_1, 1)
        GPIO.output(rly_3, 1)
        GPIO.output(rly_2, 0)
        GPIO.output(rly_4, 0)
        sleep(5)
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()
