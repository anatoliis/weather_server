import json

from datetime import datetime

from helpers import convert_pressure_to_mm, format_measurement_value
from measurement import Measurement


class MeasurementPresenter:
    def __init__(self, measurement: Measurement):
        self._measurement = measurement

    @property
    def temperature_1(self):
        return format_measurement_value(self._measurement.temperature_1)

    @property
    def temperature_2(self):
        return format_measurement_value(self._measurement.temperature_2)

    @property
    def temperature_3(self):
        return format_measurement_value(self._measurement.temperature_3)

    @property
    def avg_temperature(self):
        avg = (self._measurement.temperature_1 + self._measurement.temperature_2 + self._measurement.temperature_3) / 3.
        return format_measurement_value(avg)

    @property
    def temperature_collector(self):
        return format_measurement_value(self._measurement.temperature_collector)

    @property
    def temperature_unit(self):
        return format_measurement_value(self._measurement.temperature_unit)

    @property
    def pressure_pa(self):
        return format_measurement_value(self._measurement.pressure_pa)

    @property
    def pressure_mm(self):
        return format_measurement_value(convert_pressure_to_mm(self._measurement.pressure_pa))

    @property
    def humidity(self):
        return format_measurement_value(self._measurement.humidity)

    @property
    def timestamp(self):
        return self._measurement.time.strftime('%H:%M:%S')


class JSONMeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    def to_json(self):
        if self._measurement is None:
            return '{}'

        avg_temperature = round(
            (self._measurement.temperature_1 + self._measurement.temperature_2 + self._measurement.temperature_3) / 3,
            2
        )
        temperature_collector = self._measurement.temperature_collector
        temperature_unit = self._measurement.temperature_unit
        pressure_mm = convert_pressure_to_mm(self._measurement.pressure_pa)
        humidity = self._measurement.humidity
        date = self._measurement.time
        return json.dumps({
            'avg_temperature': format_measurement_value(avg_temperature),
            'temperature_collector': format_measurement_value(temperature_collector),
            'temperature_unit': format_measurement_value(temperature_unit),
            'pressure_mm': format_measurement_value(pressure_mm),
            'humidity': format_measurement_value(humidity),
            'timestamp': date.strftime('%H:%M:%S')
        })
