import time
import asyncio
import requests
import hashlib

from store import Store
from lines_parser import LinesParser


class WeatherController:
    def __init__(self, db_session):
        self._store = Store(db_session)
        self._lines_parser = LinesParser()

    async def get_csv_data(self, url):
        r = requests.get(url=url, timeout=7)
        return r.text

    async def get_hash(self, line):
        return hashlib.md5(line.encode('utf-8')).hexdigest()

    async def parse(self, csv_data):
        return self._lines_parser.parse(csv_data)

    async def store(self, measurements):
        new_measurements_stored = 0
        for measurement in measurements:
            new_measurements_stored += await self._store.add(measurement)
        await self._store.try_to_commit()
        return new_measurements_stored

    async def get_now(self):
        return await self._store.get_latest_measurement()

    async def get_measurements(self, last_hours=12):
        timestamp = time.time() - 12 * 3600
        measurements = await self._store.get_older_than(timestamp)
        measurements = [m.to_dict() for m in measurements]
        return measurements

    async def start(self):
        requests_counter = 0
        while True:
            request_successful = False
            new_measurements = 0
            try:
                csv_data = await self.get_csv_data('http://192.168.0.195/data_all')
                measurements = await self.parse(csv_data)                
                new_measurements = await self.store(measurements)
                requests_counter += 1
                request_successful = True
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as exc:
                pass

            timeout = 4
            if request_successful:
                if requests_counter == 0:
                    timeout = 2
                print("Request #{}. Got {} new measurement(s), next request after {} seconds..".format(
                    requests_counter, new_measurements, timeout))
            else:
                print("Error requesting data (%s), next request after %s seconds.." % (requests_counter, timeout))
            
            await asyncio.sleep(timeout)
