import asyncio
from datetime import datetime, timedelta
from time import time

import requests
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout

from data_parser import DataParser
from exceptions import DataFetchError, DataParseError
from measurement import Measurement

SENSORS_URL = 'http://192.168.0.195/data'
REQUESTS_FREQUENCY = 4
REQUEST_REPEAT_TIMEOUT = 2


class WeatherController:
    def __init__(self, db_session):
        self._db_session = db_session
        self._latest_measurement = None
        self._last_commit_timestamp = 0
        self._commit_frequency_sec = 15

    async def run(self) -> None:
        while True:
            try:
                await self.make_request()
                await asyncio.sleep(REQUESTS_FREQUENCY)
            except (DataFetchError, DataParseError) as exc:
                print(exc)
                await asyncio.sleep(REQUEST_REPEAT_TIMEOUT)

    async def make_request(self) -> None:
        csv_data = await self.get_csv_data(SENSORS_URL)
        measurement = DataParser.parse(csv_data)
        self._latest_measurement = measurement
        self._db_session.add(measurement)
        await self.commit()

    async def get_csv_data(self, url) -> str:
        try:
            return requests.get(url=url, timeout=7).text
        except (ConnectTimeout, ConnectionError, ReadTimeout) as exc:
            raise DataFetchError(exc)

    async def get_latest_measurement(self) -> Measurement:
        return self._latest_measurement

    async def get_measurements(self, last_hours=12) -> list:
        date = datetime.now() - timedelta(hours=last_hours)
        self.commit(force=True)
        measurements = self._db_session.query(Measurement).filter(
            Measurement.estimated_measurement_time >= date
        ).order_by(
            Measurement.estimated_measurement_time
        ).all()
        return self.filter_measurements(measurements)

    @staticmethod
    def filter_measurements(measurements) -> list:
        i = 0
        filtered_measurements = []
        for m in measurements:
            if i % 25 == 0:
                filtered_measurements.append(m)
            i += 1
        return filtered_measurements

    async def commit(self, force=False) -> None:
        current_time = time()
        time_passed = current_time - self._last_commit_timestamp
        if force or time_passed > self._commit_frequency_sec:
            self._db_session.commit()
            self._last_commit_timestamp = current_time
