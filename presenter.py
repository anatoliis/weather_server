from datetime import datetime


class MeasurementPresenter:
    def __init__(self, measurement):
        self._measurement = measurement

    @property
    def temperature_1(self):
        return round(self._measurement['t1'], 2)

    @property
    def temperature_2(self):
        return round(self._measurement['t2'], 2)

    @property
    def temperature_3(self):
        return round(self._measurement['t3'], 2)

    @property
    def temperature_4(self):
        return round(self._measurement['t4'], 2)

    @property
    def temperature_collector(self):
        return round(self._measurement['tc'], 2)

    @property
    def temperature_unit(self):
        return round(self._measurement['t0'], 2)

    @property
    def pressure(self):
        return round(self._measurement['pr'], 2)

    @property
    def humidity(self):
        return round(self._measurement['hm'], 2)

    @property
    def timestamp(self):
        return datetime.fromtimestamp(self._measurement['ts'])
