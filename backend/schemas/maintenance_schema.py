"""
maintenance_schema.py

Schemas for maintenance records and recommendations.
"""

from datetime import datetime
from pydantic import BaseModel


class MaintenanceResponse(BaseModel):

    machine_id: int

    maintenance_type: str

    priority: str

    engineer: str

    scheduled_date: datetime

    completion_status: str

    remarks: str

    class Config:

        from_attributes = True