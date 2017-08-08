import time


from helpers import get_minute_beginning_timestamp, calculate_real_timestamp


class Measurement:

    def __init__(self, data, mcu_fetch_timestamp):
        self._timestamp = time.time()
        self.data = data
        self._parse(mcu_fetch_timestamp)
    
    def _parse(self, mcu_fetch_timestamp):
        self.data['tc'] = round((self.data['tc'] + self.data.pop('tc2')) / 2, 2)
        real_measurement_timestamp = calculate_real_timestamp(self.data['ts'], mcu_fetch_timestamp, self._timestamp)
        rounded_real_timestamp = get_minute_beginning_timestamp(real_measurement_timestamp)
        self.data['real_measurement_timestamp'] = real_measurement_timestamp
        self.data['ts'] = rounded_real_timestamp
        self.data['power'] = 1

    @property
    def hash(self):
        return self.data['hash']

    @property
    def real_measurement_timestamp(self):
        return self.data['real_measurement_timestamp']

    def __repr__(self):
        return str(self.data)

    def __iadd__(self, other):
        if not isinstance(other, Measurement):
            raise RuntimeError("Wrong object type")
        self_ts = self.data['ts']
        other_ts = other['ts']
        if other_ts != self_ts:
            raise RuntimeError("Timestamps do not match, can't add measurements")

        total_power = self.data['power'] + other['power']
        keys = [key for key in self.data.keys() if key not in {'ml', 'ts', 'power', 'hash'}]
        for key in keys:
            self.data[key] = (self.get_powered_key(key) + other.get_powered_key(key)) / total_power
        self.data['ml'] += other['ml']
        self.data['power'] = total_power
        self.data['hash'] = None
        return self

    def get_powered_key(self, key):
        return self.data[key] * self.data['power']

    def __getitem__(self, key):
        return self.data[key]
