import time

from datetime import datetime

from measurement import Measurement
from exceptions import DataParseError


class DataParser:
    @staticmethod
    def parse(csv_data) -> Measurement:
        if csv_data is None or csv_data == '':
            raise DataParseError("empty response received: [{}]".format(csv_data))

        data = csv_data.split('\n')
        if len(data) != 3:
            raise DataParseError("invalid lines number: [{}]".format(csv_data))

        try:
            mcu_timestamp = float(data[2])
        except ValueError:
            raise DataParseError("invalid mcu timestamp: [{}]".format(csv_data))

        try:
            values = tuple(map(float, data[1].split(',')))
        except ValueError as exc:
            raise DataParseError("error parsing value: [{}], {}".format(csv_data, exc))

        measurement = Measurement()
        measurement.temperature_1 = values[0]
        measurement.temperature_2 = values[1]
        measurement.temperature_3 = values[2]
        measurement.temperature_4 = values[3]
        measurement.temperature_collector = (values[4] + values[5]) / 2
        measurement.temperature_unit = values[6]
        measurement.pressure_pa = values[7]
        measurement.humidity = values[8]
        measurement.flow_rate = values[9]
        measurement.millilitres = values[10]
        measurement.time = DataParser.calculate_real_timestamp(values[11], mcu_timestamp)
        return measurement

    @staticmethod
    def calculate_real_timestamp(mcu_measurement_timestamp, mcu_fetch_timestamp) -> datetime:
        seconds_ago = (mcu_fetch_timestamp - mcu_measurement_timestamp) / 1000. + 0.5
        return datetime.fromtimestamp(time.time() - seconds_ago)
