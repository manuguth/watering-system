"""This script reads data from a serial port, processes it and writes them to
influx DB.
"""

import serial
import json
from time import sleep
import yaml
from crate import client
import os
from datetime import datetime


import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("sensor_data.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


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


class DBCrate:
    def __init__(self):
        self.client = self._init_client()

    def _init_client(self):
        """
        Initializes the InfluxDB client with the provided configuration.
        This method is called during the initialization of the DBInflux class.
        """
        self.client = client.connect(
            os.getenv("CRATE_HOST"),
            username=os.getenv("CRATE_USERNAME"),
            password=os.getenv("CRATE_PASSWORD"),
            verify_ssl_cert=True,
        )
        logger.info("Crate client initialized")
        return self.client

    def write_measurement_to_influxdb(self, data, crate_cursor):
        query = """
        INSERT INTO sensor_data (
            timestamp,
            sensor_1,
            sensor_2,
            sensor_3,
            sensor_4,
            sensor_5,
            sensor_6,
            temperature, humidity, waterlevel
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        timestamp = datetime.utcnow()
        values = [
            timestamp,
            data["measurement"].get("sensor_1", None),
            data["measurement"].get("sensor_2", None),
            data["measurement"].get("sensor_3", None),
            data["measurement"].get("sensor_4", None),
            data["measurement"].get("sensor_5", None),
            data["measurement"].get("sensor_6", None),
            data["measurement"].get("temperature", None),
            data["measurement"].get("humidity", None),
            data["measurement"].get("waterlevel", None),
        ]
        crate_cursor.execute(query, values)


def check_humidity(sensor_data):
    pass


def main():
    # Set up the serial connection (adjust the port as needed)
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    # Define connected sensors
    # Load sensor configuration from a YAML file
    # with open("sensor_config.yaml", "r") as file:
    #     sensor_config = yaml.safe_load(file)

    # influx db setup

    db_crate = DBCrate()

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
    with db_crate.client as conn:
        cursor = conn.cursor()
        try:
            while True:
                if ser.in_waiting > 0:
                    # Read the data from the serial port
                    try:
                        data = convert_to_nested_dict(
                            ser.readline().decode("utf-8").strip()
                        )
                    except json.JSONDecodeError as e:
                        logger.error("Error decoding JSON: %s", e)
                        continue
                    except UnicodeDecodeError as e:
                        logger.error("UnicodeDecodeError: %s", e)
                        continue
                    meas_vals = data["measurement"]
                    data_points.append(meas_vals)
                    logger.debug("Count: %s", data["counter"])
                    logger.debug("%s", meas_vals)

                    time_counter += 1
                    if n_points_time == time_counter:
                        # Calculate average for each measurement key
                        avg_measurement = {}
                        for key in meas_vals:
                            # Extract all values for this key from data_points
                            values = [
                                point[key] for point in data_points if key in point
                            ]
                            # Compute average, handle empty list just in case
                            if values:
                                avg_measurement[key] = sum(values) / len(values)
                            else:
                                # avg_measurement[key] = None
                                continue

                        logger.debug("Average measurement: %s", avg_measurement)
                        avg_data = {
                            "counter": avg_counter,
                            "measurement": avg_measurement,
                        }
                        avg_counter += 1
                        db_crate.write_measurement_to_influxdb(avg_data, cursor)
                        data_points = []
                        time_counter = 0

                # Wait for a short period before the next reading
                sleep(1)

        except KeyboardInterrupt:
            # Close the serial connection
            ser.close()


if __name__ == "__main__":
    main()