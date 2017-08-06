from datetime import datetime

from helpers import convert_pressure_to_mm


class MeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    def _formatted(self, value):
        return '{:.2f}'.format(value)

    @property
    def temperature_1(self):
        return self._formatted(self._measurement['t1'])

    @property
    def temperature_2(self):
        return self._formatted(self._measurement['t2'])

    @property
    def temperature_3(self):
        return self._formatted(self._measurement['t3'])

    @property
    def avg_temperature(self):
        avg = (self._measurement['t1'] + self._measurement['t2'] + self._measurement['t3']) / 3.
        return self._formatted(avg)

    @property
    def temperature_collector(self):
        return self._formatted(self._measurement['tc'])

    @property
    def temperature_unit(self):
        return self._formatted(self._measurement['t0'])

    @property
    def pressure_pa(self):
        return self._formatted(self._measurement['pr'])

    @property
    def pressure_mm(self):
        return self._formatted(convert_pressure_to_mm(self._measurement['pr']))

    @property
    def humidity(self):
        return self._formatted(self._measurement['hm'])

    @property
    def timestamp(self):
        date = datetime.fromtimestamp(self._measurement.original_timestamp)
        return date.strftime('%H:%M:%S')
