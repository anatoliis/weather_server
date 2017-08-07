import hashlib

from datetime import datetime
from math import floor


def get_minute_beginning_timestamp(timestamp=None):
    if timestamp == None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return floor(dt.replace(second=0, microsecond=0).timestamp())


def generate_hash(line):
    return hashlib.md5(line.encode('utf-8')).hexdigest()


def convert_pressure_to_mm(value):
    return round(value / 133.3223684, 2)
