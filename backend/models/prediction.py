"""
Prediction Model
Stores AI prediction results.
"""

from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime
from backend.database import Base
from datetime import datetime


class Prediction(Base):

    __tablename__="predictions"

    id = Column(Integer, primary_key=True, index=True)

    machine_id=Column(Integer,ForeignKey("machines.id"))

    health_score=Column(Float)

    failure_probability=Column(Float)

    risk_level=Column(String)

    predicted_failure=Column(String)

    estimated_failure_days=Column(Integer)

    confidence_score=Column(Float)

    generated_at=Column(DateTime,default=datetime.utcnow)