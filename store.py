import time
import transaction

from datetime import datetime
from sqlalchemy import exists

from measurement_model import Measurement
from dynamic_store import DynamicStore
from helpers import get_minute_beginning_timestamp


class Store():
    def __init__(self, db_session):
        self._db_session = db_session
        self._last_commit_timestamp = time.time()
        self._ram_storage = DynamicStore()
        self._commit_timeout = 300

    async def add(self, measurement):
        old_length = len(self._ram_storage)
        self._ram_storage.add(measurement)
        new_length = len(self._ram_storage)
        return new_length - old_length

    async def get_latest_measurement(self):
        return self._ram_storage.get_latest()

    async def get_older_than(self, timestamp):
        return self._db_session.query(
            Measurement
        ).filter(
            Measurement.time >= timestamp
        ).all()

    async def try_to_commit(self):
        current_timestamp = time.time()
        time_left_to_save = self._commit_timeout - (current_timestamp - self._last_commit_timestamp)

        if time_left_to_save <= 0:
            self._last_commit_timestamp = current_timestamp
            print('Committing..')
            return await self._save_from_ram_to_db()
        else:
            print('Time left to commit: {} sec'.format(round(time_left_to_save, 2)))
        return False 

    async def _save_from_ram_to_db(self):
        current_minute_start = get_minute_beginning_timestamp()
        measurements_to_store = self._ram_storage.extract_everything_older_than(current_minute_start - 240)
        measurements = [self.create_measurement(m) for m in measurements_to_store]
        await self.store_to_db(measurements)

    @staticmethod
    def create_measurement(measurement):
        names = ['t1', 't2', 't3', 't4', 'tc', 't0', 'pr', 'hm', 'fr', 'ml']
        values = [round(measurement[key], 2) for key in names]
        kwargs = dict(zip(names, values))
        return Measurement(**kwargs, time=datetime.fromtimestamp(measurement['ts']))

    async def store_to_db(self, measurements):
        for measurement in measurements:
            already_exists = self._db_session.query(exists().where(Measurement.time == measurement.time)).scalar()
            if not already_exists:
                self._db_session.add(measurement)
            else:
                print("Tried to add an existing measurement", measurement)
        transaction.commit()
