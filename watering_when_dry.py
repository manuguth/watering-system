import serial
import time
import ast
import RPi.GPIO as GPIO
from time import sleep

def convert_to_nested_dict(input_str):
    # Use ast.literal_eval to safely evaluate the string as a Python literal
    nested_dict = ast.literal_eval(input_str)
    return nested_dict

def main():
    # Set up the serial connection (adjust the port as needed)
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    # setup GPIO
    rly_1 = 16 # IN1 on relay: blue LED
    rly_2 = 20 # IN2 on relay: green LED
    rly_3 = 21 # IN3 on relay: pump
    rly_4 = 4 # IN4 on relay: red LED
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rly_1, GPIO.OUT)
    GPIO.setup(rly_2, GPIO.OUT)
    GPIO.setup(rly_3, GPIO.OUT)
    GPIO.setup(rly_4, GPIO.OUT)

    rly_status_3 = 1

    GPIO.output(rly_1, 1)
    GPIO.output(rly_2, 1)
    GPIO.output(rly_3, rly_status_3)
    GPIO.output(rly_4, 1)



    try:
        while True:
            if ser.in_waiting > 0:
                # Read the data from the serial port
                data = convert_to_nested_dict(ser.readline().decode('utf-8').strip())
                meas_vals = data["measurement"]
                print(meas_vals)
                if meas_vals["sensor_1"] < 50 and rly_status_3==1:
                    GPIO.output(rly_3, 0) # turn on pump
                    GPIO.output(rly_1, 0) # turn on blue LED
                    rly_status_3 = 0
                elif meas_vals["sensor_1"] >= 50 and rly_status_3==0:
                    GPIO.output(rly_3, 1) # turn off pump
                    GPIO.output(rly_1, 1) # turn off blue LED
                    rly_status_3 = 1

            # Wait for a short period before the next reading
            sleep(1)

    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()
        GPIO.cleanup()


if __name__ == "__main__":
    main()




# try:
#     while True:
#         # print("set to 0")
#         # GPIO.output(rly_1, 1)
#         # GPIO.output(rly_2, 0)
#         # GPIO.output(rly_3, 1)
#         # sleep(20)
#         # print("set to 1")
#         # GPIO.output(rly_1, 0)
#         # GPIO.output(rly_2, 1)
#         # GPIO.output(rly_3, 0)
#         # sleep(8)

#         GPIO.output(rly_1, 0)
#         GPIO.output(rly_3, 0)
#         GPIO.output(rly_2, 1)
#         GPIO.output(rly_4, 1)
#         sleep(5)
#         GPIO.output(rly_1, 1)
#         GPIO.output(rly_3, 1)
#         GPIO.output(rly_2, 0)
#         GPIO.output(rly_4, 0)
#         sleep(5)
# except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
#     GPIO.cleanup()
