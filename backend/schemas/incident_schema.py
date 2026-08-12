"""
incident_schema.py

Schema for machine incidents.
"""

from pydantic import BaseModel


class IncidentResponse(BaseModel):

    machine_id: int

    incident_type: str

    severity: str

    root_cause: str

    description: str

    action_taken: str

    resolved_status: str

    class Config:

        from_attributes = True