"""
Maintenance Model
Stores maintenance history.
"""

from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from backend.database import Base
from datetime import datetime


class Maintenance(Base):

    __tablename__="maintenance"

    id = Column(Integer, primary_key=True, index=True)

    machine_id=Column(Integer,ForeignKey("machines.id"))

    maintenance_type=Column(String)

    priority=Column(String)

    engineer=Column(String)

    scheduled_date=Column(DateTime)

    completion_status=Column(String)

    remarks=Column(String)

    created_at=Column(DateTime,default=datetime.utcnow)