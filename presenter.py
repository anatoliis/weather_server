import json

from datetime import datetime

from helpers import convert_pressure_to_mm, format_measurement_value


class MeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    @property
    def temperature_1(self):
        return format_measurement_value(self._measurement['t1'])

    @property
    def temperature_2(self):
        return format_measurement_value(self._measurement['t2'])

    @property
    def temperature_3(self):
        return format_measurement_value(self._measurement['t3'])

    @property
    def avg_temperature(self):
        avg = (self._measurement['t1'] + self._measurement['t2'] + self._measurement['t3']) / 3.
        return format_measurement_value(avg)

    @property
    def temperature_collector(self):
        return format_measurement_value(self._measurement['tc'])

    @property
    def temperature_unit(self):
        return format_measurement_value(self._measurement['t0'])

    @property
    def pressure_pa(self):
        return format_measurement_value(self._measurement['pr'])

    @property
    def pressure_mm(self):
        return format_measurement_value(convert_pressure_to_mm(self._measurement['pr']))

    @property
    def humidity(self):
        return format_measurement_value(self._measurement['hm'])

    @property
    def timestamp(self):
        date = datetime.fromtimestamp(self._measurement.real_measurement_timestamp)
        return date.strftime('%H:%M:%S')


class JSONMeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    def to_json(self):
        print(self._measurement)
        avg_temperature = round((self._measurement['t1'] + self._measurement['t2'] + self._measurement['t3']) / 3, 2)
        temperature_collector = self._measurement['tc']
        temperature_unit = self._measurement['t0']
        pressure_mm = convert_pressure_to_mm(self._measurement['pr'])
        humidity = self._measurement['hm']
        date = datetime.fromtimestamp(self._measurement.real_measurement_timestamp)
        timestamp = date.strftime('%H:%M:%S')
        return json.dumps({
            'avg_temperature': format_measurement_value(avg_temperature),
            'temperature_collector': format_measurement_value(temperature_collector),
            'temperature_unit': format_measurement_value(temperature_unit),
            'pressure_mm': format_measurement_value(pressure_mm),
            'humidity': format_measurement_value(humidity),
            'timestamp': timestamp
        })
