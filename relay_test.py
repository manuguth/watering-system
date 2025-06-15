import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

rly = 13
GPIO.setup(rly, GPIO.OUT)
GPIO.output(rly, 1)



try:
    while True:
        sleep(10)
        print("set to 0")
        GPIO.output(rly, 0)
        sleep(10)
        print("set to 1")
        GPIO.output(rly, 1)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()