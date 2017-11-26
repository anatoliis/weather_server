from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    create_engine
)
from sqlite3 import dbapi2 as sqlite

from helpers import convert_pressure_to_mm

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
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<Measurement timestamp={}>".format(self.time)

    def to_dict(self):
        return {
            'temperature_1': self.temperature_1,
            'temperature_2': self.temperature_2,
            'temperature_3': self.temperature_3,
            'avg_temperature': (self.temperature_1 + self.temperature_2 + self.temperature_3) / 3,
            'temperature_collector': self.temperature_collector,
            'temperature_unit': self.temperature_unit,
            'pressure_pa': self.pressure_mm,
            'pressure_mm': convert_pressure_to_mm(self.pressure_mm),
            'humidity': self.humidity,
            'timestamp': self.time.timestamp()
        }


engine = create_engine('sqlite:///weather01.db', module=sqlite)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker())
db_session.configure(bind=engine)
db_session = db_session()
