import time

from measurement_line import MeasurementLine
from helpers import get_minute_beginning_timestamp


class DynamicStore:
    def __init__(self):
        self.data = {}
        self._old_hashes = set()
        self._hashes = set()
        self._clear_hashes_timestamp = time.time()

    def add(self, measurement):
        if self._hash_is_present(measurement.hash):
            return False
        self._hashes.add(measurement.hash)
        timestamp = measurement['ts']
        if timestamp in self.data.keys():
            self.data[timestamp] += measurement
        else:
            self.data[timestamp] = measurement
        return True

    def get_latest(self):
        max_timestamp = max(self.data.keys())
        return self.data[max_timestamp]

    def extract_everything_older_than(self, timestamp):
        extracted = []
        keys = tuple(self.data.keys())
        for key in keys:
            if key < timestamp:
                extracted.append(self.data.pop(key))
        self._clear_hashes()
        return extracted

    def _clear_hashes(self):
        timestamp = time.time()
        if timestamp - self._clear_hashes_timestamp > 300:
            self._old_hashes = self._hashes
            self._hashes = set()
            self._clear_hashes_timestamp = timestamp

    def _hash_is_present(self, m_hash):
        return m_hash in self._hashes or m_hash in self._old_hashes

    def __len__(self):
        length = 0
        for key in self.data.keys():
            length += self.data[key]['power']
        return length

    def __str__(self):
        return str(self.data)
