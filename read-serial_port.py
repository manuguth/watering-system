import time
import serial
import json
from crate import client
from datetime import datetime

import os

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


def write_measurement_to_cratedb(data, crate_cursor):
    query = """
    INSERT INTO sensor_data (
        timestamp,
        sensor_1, sensor_raw_1,
        sensor_2, sensor_raw_2,
        sensor_3, sensor_raw_3,
        sensor_4, sensor_raw_4,
        sensor_5, sensor_raw_5,
        sensor_6, sensor_raw_6,
        temperature, humidity, waterlevel
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    timestamp = datetime.utcnow()
    values = [
        timestamp,
        data["measurement"].get("sensor_1", None),
        data["measurement"].get("sensor_raw_1", None),
        data["measurement"].get("sensor_2", None),
        data["measurement"].get("sensor_raw_2", None),
        data["measurement"].get("sensor_3", None),
        data["measurement"].get("sensor_raw_3", None),
        data["measurement"].get("sensor_4", None),
        data["measurement"].get("sensor_raw_4", None),
        data["measurement"].get("sensor_5", None),
        data["measurement"].get("sensor_raw_5", None),
        data["measurement"].get("sensor_6", None),
        data["measurement"].get("sensor_raw_6", None),
        data["measurement"].get("temperature", None),
        data["measurement"].get("humidity", None),
        data["measurement"].get("waterlevel", None)
    ]
    crate_cursor.execute(query, values)

# Set up the serial connection (adjust the port as needed)
ser = serial.Serial("/dev/ttyUSB0", 9600)

conn = client.connect(
    os.getenv("CRATE_HOST"),
    username=os.getenv("CRATE_USERNAME"),
    password=os.getenv("CRATE_PASSWORD"),
    verify_ssl_cert=True,
)

with conn:
    cursor = conn.cursor()
    try:
        while True:
            if ser.in_waiting > 0:
                # Read the data from the serial port
                ser_data = ser.readline().decode("utf-8").strip()
                data = convert_to_nested_dict(ser_data)
                # print(data["counter"])
                # print(data["measurement"])
                # print("=" * 20)
                # Write the measurement data to InfluxDB
                write_measurement_to_cratedb(data, cursor)

            # Wait for a short period before the next reading
            time.sleep(5)

    except KeyboardInterrupt:
        # Close the serial connection
        ser.close()

    cursor.close()
