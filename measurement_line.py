import time
import hashlib


from helpers import get_minute_beginning_timestamp


class MeasurementLine:
    def __init__(self, names, line, mc_timestamp):
        self.data = None
        self.hash = None
        self.original_timestamp = None
        self._parse(line, names, mc_timestamp)
    
    def _parse(self, line, names, mc_timestamp):
        parse_timestamp = time.time()
        self._generate_hash(line)
        values = list(map(float, line.split(',')))
        data = dict(zip(names, values))
        self.original_timestamp = self._get_timestamp(data['ts'], parse_timestamp, mc_timestamp)
        data['ts'] = get_minute_beginning_timestamp(self.original_timestamp)
        data['power'] = 1
        self.data = data

    def to_dict(self):
        return self.data

    def _generate_hash(self, line):
        self.hash = hashlib.md5(line.encode('utf-8')).hexdigest()

    def _get_timestamp(self, measurement_timestamp, parse_timestamp, mc_timestamp):
        seconds_ago = (mc_timestamp - measurement_timestamp) / 1000. + 1
        timestamp = parse_timestamp - seconds_ago
        return timestamp

    def __repr__(self):
        return str(self.data)

    def __iadd__(self, other):
        if not isinstance(other, MeasurementLine):
            raise RuntimeError("Wrong object type")
        self_ts = self.data['ts']
        other_ts = other['ts']
        if other_ts != self_ts:
            raise RuntimeError("Timestamps do not match, can't add measurements")

        total_power = self.data['power'] + other['power']
        keys = [key for key in self.data.keys() if key not in ('ml', 'ts', 'power')]
        for key in keys:
            self.data[key] = (self.get_powered_key(key) + other.get_powered_key(key)) / total_power
        self.data['ml'] += other['ml']
        self.data['power'] = total_power
        self.hash = None
        return self

    def get_powered_key(self, key):
        return self.data[key] * self.data['power']

    def __getitem__(self, key):
        return self.data[key]
