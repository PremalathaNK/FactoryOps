"""
Incident Model
Stores machine failure incidents.
"""

from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from backend.database import Base
from datetime import datetime


class Incident(Base):

    __tablename__="incidents"

    id = Column(Integer, primary_key=True, index=True)

    machine_id=Column(Integer,ForeignKey("machines.id"))

    incident_type=Column(String)

    severity=Column(String)

    root_cause=Column(String)

    description=Column(String)

    action_taken=Column(String)

    reported_time=Column(DateTime,default=datetime.utcnow)

    resolved_status=Column(String,default="Pending")