"""This module parse one line of raw serial data from ojbot."""

import re

def to_numbers(line):
    """Parse a line in format of "b'0,101,152.00\r\n'". """
    parsed_str = re.findall(r'(\d+(?:\.\d+)?)', line)
    if len(parsed_str) != 3:
        return (False, '[Error] There are not exactly 3 numbers.', parsed_str)
    parsed_number = [0, 0, 0]
    try:
        parsed_number = [float(str) for str in parsed_str]
    except ValueError:
        return (False, '[Error] Some numbers cannot be parsed.', parsed_str)
    return (True, parsed_number)

# """Test"""
# import serial
# ser = serial.Serial('/dev/cu.usbmodem1411', 115200)
# while True:
#     line = ser.readline().decode('utf-8')
#     print(to_numbers(line))
