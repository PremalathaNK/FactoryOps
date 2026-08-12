"""
Sensor Model
Stores sensor values collected from machines.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from backend.database import Base
from datetime import datetime


class Sensor(Base):

    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(Integer, ForeignKey("machines.id"))

    temperature = Column(Float)

    vibration = Column(Float)

    pressure = Column(Float)

    humidity = Column(Float)

    voltage = Column(Float)

    current = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)