import RPi.GPIO as GPIO
from time import sleep

rly_1 = 26 # IN1 on relay: yellow LED
rly_2 = 19 # IN2 on relay: blue LED
rly_3 = 21 # IN3 on relay: greenLED
rly_4 = 20 # IN4 on relay: red LED
rly_5 = 13, # 12V single relay: pump
GPIO.setmode(GPIO.BCM)
GPIO.setup(rly_1, GPIO.OUT)
GPIO.setup(rly_2, GPIO.OUT)
GPIO.setup(rly_3, GPIO.OUT)
GPIO.setup(rly_4, GPIO.OUT)
GPIO.setup(rly_5, GPIO.OUT)
GPIO.output(rly_1, 1)
GPIO.output(rly_2, 1)
GPIO.output(rly_3, 1)
GPIO.output(rly_4, 1)
GPIO.output(rly_5, 0)

# sleep(10)
try:
    GPIO.output(rly_5, 1)  # Turn on the pump
    # sleep(3)
    while True:
        # GPIO.output(rly_1, 0)
        # GPIO.output(rly_1, 1)
        # GPIO.output(rly_3, 1)

        # GPIO.output(rly_4, 0)
        # GPIO.output(rly_2, 0)

        # sleep(30)
        # # GPIO.output(rly_1, 1)
        # GPIO.output(rly_4, 1)
        # GPIO.output(rly_2, 1)

        # GPIO.output(rly_1, 0)
        # GPIO.output(rly_3, 0)

        sleep(30)

    # GPIO.output(rly_5, 0)  # Turn off the pump
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()


