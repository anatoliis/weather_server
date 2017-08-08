import time
import asyncio
import requests

from requests.exceptions import ConnectTimeout, ConnectionError

from store import Store
from csv_data_parser import parser


SENSORS_URL = 'http://192.168.0.195/data_all'
REQUESTS_FREQUENCY = 4
REQUEST_REPEAT_TIMEOUT = 2


class WeatherController:
    def __init__(self, db_session):
        self._store = Store(db_session)
        self._requests_made = 0

    @staticmethod
    async def _get_csv_data(url):
        try:
            r = requests.get(url=url, timeout=7)
            return r.text
        except (ConnectTimeout, ConnectionError) as exc:
            print('Error getting data from sensors: {}, repeat after {} sec...'.format(
                exc, REQUEST_REPEAT_TIMEOUT))

    async def store(self, measurements):
        new_measurements_stored = 0
        for measurement in measurements:
            new_measurements_stored += await self._store.add(measurement)
        await self._store.try_to_commit()
        return new_measurements_stored

    async def get_now(self):
        return await self._store.get_latest_measurement()

    async def get_measurements(self, last_hours=12):
        timestamp = time.time() - last_hours * 3600
        measurements = await self._store.get_after_timestamp(timestamp)
        measurements = [m.to_dict() for m in measurements]
        return measurements

    async def make_request(self):
        csv_data = await self._get_csv_data(SENSORS_URL)
        if csv_data is None:
            return False
        measurements = parser.parse(csv_data)
        new_measurements_number = await self.store(measurements)
        self._requests_made += 1

        print("Request #{}. Got {} new measurement(s), next request after {} seconds..".format(
            self._requests_made, new_measurements_number, REQUESTS_FREQUENCY)
        )
        return new_measurements_number != 0

    async def run(self):
        while True:
            is_successful = await self.make_request()
            timeout = REQUESTS_FREQUENCY if is_successful else REQUEST_REPEAT_TIMEOUT

            await asyncio.sleep(timeout)
