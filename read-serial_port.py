import serial
import time
import ast

def convert_to_nested_dict(input_str):
    # Use ast.literal_eval to safely evaluate the string as a Python literal
    nested_dict = ast.literal_eval(input_str)
    return nested_dict


# Set up the serial connection (adjust the port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600)

try:
    while True:
        if ser.in_waiting > 0:
            # Read the data from the serial port
            data = convert_to_nested_dict(ser.readline().decode('utf-8').strip())
            # print(f"Received data: {data}")
            # print(f"Received data: {nested_dict}")
            print(data["counter"])
            print(data["measurement"])

        # Wait for a short period before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial connection
    ser.close()
