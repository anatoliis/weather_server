import json
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import (
    Column,
    Integer,
    Float,
    BigInteger,
    DateTime,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import convert_pressure_to_mm, average_temperature

Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    temperature_1 = Column(Float, nullable=False)
    temperature_2 = Column(Float, nullable=False)
    temperature_3 = Column(Float, nullable=False)
    temperature_4 = Column(Float, nullable=False)
    temperature_collector = Column(Float, nullable=False)
    temperature_unit = Column(Float, nullable=False)
    pressure_pa = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    flow_rate = Column(Integer, nullable=False)
    millilitres = Column(Integer, nullable=False)
    mcu_timestamp = Column(BigInteger, nullable=False, unique=True)
    estimated_measurement_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<Measurement timestamp={}>".format(self.time)

    def get_avg_temperature(self):
        return average_temperature([self.temperature_1, self.temperature_2, self.temperature_3])

    def to_dict(self):
        return {
            'avg_temperature': self.format_value(self.get_avg_temperature()),
            'temperature_collector': self.format_value(self.temperature_collector),
            'pressure_mm': self.format_value(convert_pressure_to_mm(self.pressure_pa)),
            'humidity': self.format_value(self.humidity),
            'timestamp': self.estimated_measurement_time.strftime('%H:%M:%S')
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def format_value(value) -> str:
        return '{:.2f}'.format(value)


engine = create_engine('sqlite:///weather01.db', module=sqlite)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker())
db_session.configure(bind=engine)
db_session = db_session()
