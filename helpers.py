import hashlib

from datetime import datetime
from math import floor


def get_minute_beginning_timestamp(timestamp=None):
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return floor(dt.replace(second=0, microsecond=0).timestamp())


def calculate_real_timestamp(mcu_measurement_timestamp, mcu_fetch_timestamp, received_real_timestamp):
    seconds_ago = (mcu_fetch_timestamp - mcu_measurement_timestamp) / 1000. + 0.5
    return received_real_timestamp - seconds_ago


def generate_hash(line):
    return hashlib.md5(line.encode('utf-8')).hexdigest()


def convert_pressure_to_mm(value):
    return round(value / 133.3223684, 2)


def format_measurement_value(value) -> str:
    return '{:.2f}'.format(value)


def average_temperature(temperatures_list):
    number_of_values = 0
    sum_of_values = 0
    for t in temperatures_list:
        if not temperature_is_valid(t):
            continue
        number_of_values += 1
        sum_of_values += t

    return sum_of_values / number_of_values


def temperature_is_valid(temperature) -> bool:
    return temperature in range(-50, 120)
