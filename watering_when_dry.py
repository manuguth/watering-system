""" " This script reads data from a serial port, processes it, and controls GPIO pins on
a Raspberry Pi to manage a watering system based on sensor readings.
It uses the RPi.GPIO library to control GPIO pins and the serial library to communicate
with a serial device. The script continuously reads data from the serial port, checks
the sensor values, and turns on or off a pump and LEDs based on the readings.
"""

import serial
import time
import json
import RPi.GPIO as GPIO
from time import sleep
import yaml
from influxdb import InfluxDBClient
from datetime import datetime


def convert_to_nested_dict(input_str):
    """
    Converts a string representation of a nested dictionary into an actual nested
    dictionary. This function replaces single quotes in the input string with double
    quotes to ensure it adheres to JSON format, then uses `json.loads` to parse the
    string into a dictionary.
    Parameters
    ----------
    input_str : str
        A string representation of a nested dictionary. The string must use single
        quotes for keys and values.
    Returns
    -------
    dict
        A nested dictionary parsed from the input string.
    Raises
    ------
    json.JSONDecodeError
        If the input string is not a valid JSON format after replacing single quotes
        with double quotes.
    """
    input_str = input_str.replace("'", '"')
    nested_dict = json.loads(input_str)
    return nested_dict


class DBInflux:
    def __init__(
        self,
        host,
        port,
        username,
        password,
        database,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = self._init_client()

    def _init_client(self):
        """
        Initializes the InfluxDB client with the provided configuration.
        This method is called during the initialization of the DBInflux class.
        """
        self.client = InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )
        print("InfluxDB client initialized")
        return self.client

    def write_measurement_to_influxdb(self, data):
        json_body = [
            {
                "measurement": "sensor_measurement",
                "tags": {"counter": data["counter"]},
                "fields": data["measurement"],
            }
        ]
        # Write the data to InfluxDB
        self.client.write_points(json_body)


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
        "rly_1": 26, # IN1 on relay: yellow LED
        "rly_2": 19, # IN2 on relay: blue LED
        "rly_3": 21, # IN3 on relay: greenLED
        "rly_4": 20, # IN4 on relay: red LED
        "rly_5": 13, # 12V single relay: pump

    }
    GPIO.setmode(GPIO.BCM)
    for key, rly in rlys.items():
        # Setup GPIO pins for relays
        GPIO.setup(rly, GPIO.OUT)
        # Set the initial state of the relays to off
        GPIO.output(rly, 1 if key != "rly_5" else 0)

    # flags for pump and relay status
    # by default, pump is off
    pump_needed = {key: False for key in sensor_config.keys()}
    pump_rly_status = 0

    # influx db setup

    infl_db = DBInflux(
        host="localhost",
        port=8086,
        username="grafana",
        password="blacony-watering",
        database="plant_monitoring",
    )

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the data from the serial port
                try:
                    data = convert_to_nested_dict(ser.readline().decode("utf-8").strip())
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    continue
                except UnicodeDecodeError as e:
                    print("UnicodeDecodeError:", e)
                    continue
                meas_vals = data["measurement"]
                print("Count:", data["counter"])
                print(meas_vals)
                infl_db.write_measurement_to_influxdb(data)
                continue

                for sensor, elem in sensor_config.items():
                    # Check if the sensor value is below the threshold
                    if meas_vals[sensor] < elem["threshold"]:
                        pump_needed[sensor] = True
                        GPIO.output(elem["gpio_relay"], 0)  # turn on LED
                    else:
                        pump_needed[sensor] = False
                        GPIO.output(elem["gpio_relay"], 1)
                # Check if the pump is needed for any sensor
                if any(pump_needed.values()) and pump_rly_status == 0:
                    pump_rly_status = 1
                    GPIO.output(rlys["rly_5"], pump_rly_status)
                elif not any(pump_needed.values()) and pump_rly_status == 1:
                    # If no sensor needs the pump, turn it off
                    # but only if it was on
                    # and the pump relay is on
                    pump_rly_status = 0
                    GPIO.output(rlys["rly_5"], pump_rly_status)

            # Wait for a short period before the next reading
            sleep(1)

    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
