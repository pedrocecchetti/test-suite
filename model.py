from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TestRun(Base):
    __tablename__ = 'test_run'

    id = Column(Integer, primary_key=True)
    enviroment = Column(String)
    test = Column(String)
    created_at = Column(DateTime)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    status = Column(Text)
    logs = Column(Text)