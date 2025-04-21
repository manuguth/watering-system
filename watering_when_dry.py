"""" This script reads data from a serial port, processes it, and controls GPIO pins on
a Raspberry Pi to manage a watering system based on sensor readings.
It uses the RPi.GPIO library to control GPIO pins and the serial library to communicate
with a serial device. The script continuously reads data from the serial port, checks
the sensor values, and turns on or off a pump and LEDs based on the readings.
"""
import serial
import time
import ast
import RPi.GPIO as GPIO
from time import sleep
import yaml


def convert_to_nested_dict(input_str):
    # Use ast.literal_eval to safely evaluate the string as a Python literal
    nested_dict = ast.literal_eval(input_str)
    return nested_dict

def check_humidity(sensor_data):
    pass

def main():
    # Set up the serial connection (adjust the port as needed)
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    # Define connected sensors
    # Load sensor configuration from a YAML file
    with open("sensor_config.yaml", "r") as file:
        sensor_config = yaml.safe_load(file)
    # for now map sensors to GPIO pins for LEDs, later need to add valves
    # sensors = {
    #     "sensor_1": 16,
    #     "sensor_2": 20,
    #     "sensor_3": 4,
    # }
    # setup GPIO relay pins
    rlys = {
        "rly_1": 16,  # IN1 on relay: blue LED
        "rly_2": 20,  # IN2 on relay: green LED
        "rly_3": 21,  # IN3 on relay: pump
        "rly_4": 4,  # IN4 on relay: red LED
    }
    GPIO.setmode(GPIO.BCM)
    for rly in rlys.values():
        GPIO.setup(rly, GPIO.OUT)
        # Set the initial state of the relays to off
        GPIO.output(rly, 1)

    # flags for pump and relay status
    # by default, pump is off
    pump_needed = {key: False for key in sensor_config.keys()}
    pump_rly_status = 1

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the data from the serial port
                data = convert_to_nested_dict(ser.readline().decode("utf-8").strip())
                meas_vals = data["measurement"]
                print("Count:", data["counter"])
                print(meas_vals)

                for sensor, elem in sensor_config.items():
                    # Check if the sensor value is below the threshold
                    if meas_vals[sensor] < elem["threshold"]:
                        pump_needed[sensor] = True
                        GPIO.output(elem["gpio_relay"], 0)  # turn on LED
                    else:
                        pump_needed[sensor] = False
                        GPIO.output(elem["gpio_relay"], 1)
                # Check if the pump is needed for any sensor
                if any(pump_needed.values()) and pump_rly_status==1:
                    pump_rly_status = 0
                    GPIO.output(rlys["rly_3"], pump_rly_status)
                elif not any(pump_needed.values()) and pump_rly_status==0:
                    # If no sensor needs the pump, turn it off
                    # but only if it was on
                    # and the pump relay is on
                    pump_rly_status = 1
                    GPIO.output(rlys["rly_3"], pump_rly_status)


            # Wait for a short period before the next reading
            sleep(1)

    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
