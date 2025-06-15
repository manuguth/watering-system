""" This script reads data from a serial port, processes it and writes them to
    influx DB.
"""

import serial
import json
from time import sleep
import yaml
from influxdb import InfluxDBClient


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

    # influx db setup

    infl_db = DBInflux(
        host="localhost",
        port=8086,
        username="grafana",
        password="blacony-watering",
        database="plant_monitoring",
    )

    time_counter = 0
    avg_counter = 0
    # define how many time points are averaged over
    n_points_time = 10
    meas_vals = [
                "sensor_1",
                "sensor_2",
                "sensor_3",
                "sensor_4",
                "temperature",
                "humidity",
                "waterlevel",
                ]
    data_points = []
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
                data_points.append(meas_vals)
                print("Count:", data["counter"])
                print(meas_vals)

                time_counter += 1
                if n_points_time == time_counter:

                     # Calculate average for each measurement key
                    avg_measurement = {}
                    for key in meas_vals:
                        # Extract all values for this key from data_points
                        values = [point[key] for point in data_points if key in point]
                        # Compute average, handle empty list just in case
                        if values:
                            avg_measurement[key] = sum(values) / len(values)
                        else:
                            # avg_measurement[key] = None
                            continue

                    print("Average measurement:", avg_measurement)
                    avg_data = {
                        "counter": avg_counter,
                        "measurement": avg_measurement
                    }
                    avg_counter += 1
                    infl_db.write_measurement_to_influxdb(avg_data)
                    data_points = []
                    time_counter = 0

            # Wait for a short period before the next reading
            sleep(1)

    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()


if __name__ == "__main__":
    main()
