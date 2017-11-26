import asyncio
from datetime import datetime, timedelta

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
        self._requests_made = 0
        self._latest_measurement = None

    async def run(self):
        while True:
            try:
                await self.make_request()
                await asyncio.sleep(REQUESTS_FREQUENCY)
            except (DataFetchError, DataParseError) as exc:
                print(exc)
                await asyncio.sleep(REQUEST_REPEAT_TIMEOUT)

    async def make_request(self):
        csv_data = await self.get_csv_data(SENSORS_URL)
        measurement = DataParser.parse(csv_data)
        self._latest_measurement = measurement
        self._db_session.add(measurement)
        self._db_session.commit()

    async def get_csv_data(self, url):
        try:
            return requests.get(url=url, timeout=7).text
        except (ConnectTimeout, ConnectionError, ReadTimeout) as exc:
            raise DataFetchError(exc)

    async def get_latest_measurement(self):
        return self._latest_measurement

    async def get_measurements(self, last_hours=12):
        date = datetime.now() - timedelta(hours=12)
        measurements = self._db_session.query(Measurement).filter(
            Measurement.estimated_measurement_time >= date
        ).order_by(
            Measurement.estimated_measurement_time
        ).all()
        return measurements
