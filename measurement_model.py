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

Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    t1 = Column(Float, nullable=False)
    t2 = Column(Float, nullable=False)
    t3 = Column(Float, nullable=False)
    t4 = Column(Float, nullable=False)
    tc = Column(Float, nullable=False)
    t0 = Column(Float, nullable=False)
    pr = Column(Float, nullable=False)
    hm = Column(Float, nullable=False)
    fr = Column(Integer, nullable=False)
    ml = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<Measurement timestamp={}>".format(self.time)


engine = create_engine('sqlite:///weather01.db', module=sqlite)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
db_session.configure(bind=engine)
db_session = db_session()
