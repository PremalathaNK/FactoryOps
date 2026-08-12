"""
sensor_schema.py

Validates incoming sensor values
before storing them into the database.
"""

from pydantic import BaseModel, Field


class SensorCreate(BaseModel):

    machine_id: int

    temperature: float = Field(..., ge=-20, le=150)

    vibration: float = Field(..., ge=0, le=50)

    pressure: float = Field(..., ge=0, le=300)

    humidity: float = Field(..., ge=0, le=100)

    voltage: float = Field(..., ge=0, le=500)

    current: float = Field(..., ge=0, le=100)


class SensorResponse(SensorCreate):

    id: int

    class Config:

        from_attributes = True