import serial
import time
import json
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


# Function to write measurement data to InfluxDB
def write_measurement_to_influxdb(data, influx_client):
    json_body = [
        {
            "measurement": "sensor_measurement",
            "tags": {"counter": data["counter"]},
            "fields": data["measurement"],
            "time": datetime.utcnow().isoformat(),
        }
    ]

    # Write the data to InfluxDB
    influx_client.write_points(json_body)


# Set up the serial connection (adjust the port as needed)
ser = serial.Serial("/dev/ttyUSB0", 9600)

# Configuration for InfluxDB
host = "localhost"
port = 8086
username = "grafana"
password = "blacony-watering"
database = "plant_monitoring"

# Initialize the InfluxDB client
client = InfluxDBClient(
    host=host, port=port, username=username, password=password, database=database
)


try:
    while True:
        if ser.in_waiting > 0:
            # Read the data from the serial port
            ser_data = ser.readline().decode("utf-8").strip()
            data = convert_to_nested_dict(ser_data)
            print(data["counter"])
            print(data["measurement"])
            print("=" * 20)
            # Write the measurement data to InfluxDB
            write_measurement_to_influxdb(data, client)

        # Wait for a short period before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial connection
    ser.close()
