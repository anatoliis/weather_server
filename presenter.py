from datetime import datetime


class MeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    @property
    def temperature_1(self):
        return '{:.2f}'.format(self._measurement['t1'])

    @property
    def temperature_2(self):
        return '{:.2f}'.format(self._measurement['t2'])

    @property
    def temperature_3(self):
        return '{:.2f}'.format(self._measurement['t3'])

    @property
    def avg_temperature(self):
        avg = (self._measurement['t1'] + self._measurement['t2'] + self._measurement['t3']) / 3.
        return '{:.2f}'.format(avg)

    @property
    def temperature_collector(self):
        return '{:.2f}'.format(self._measurement['tc'])

    @property
    def temperature_unit(self):
        return '{:.2f}'.format(self._measurement['t0'])

    @property
    def pressure_pa(self):
        return '{:.2f}'.format(self._measurement['pr'])

    @property
    def pressure_mm(self):
        return '{:.2f}'.format(self._measurement['pr'] / 133.3223684)

    @property
    def humidity(self):
        return '{:.2f}'.format(self._measurement['hm'])

    @property
    def timestamp(self):
        date = datetime.fromtimestamp(self._measurement.original_timestamp)

        return date.strftime('%H:%M:%S')
