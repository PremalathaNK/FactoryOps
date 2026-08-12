from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MachineCreate(BaseModel):

    machine_code: str = Field(
        ...,
        min_length=3,
        max_length=20
    )

    machine_name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    machine_type: str

    department: str

    installation_date: Optional[datetime] = None

    operating_hours: float = Field(
        ...,
        ge=0
    )

    health_status: str = "Healthy"

    last_service_date: Optional[datetime] = None


class MachineResponse(BaseModel):

    id: int

    machine_code: str

    machine_name: str

    machine_type: str

    department: str

    installation_date: Optional[datetime] = None

    operating_hours: float

    health_status: str

    last_service_date: Optional[datetime] = None

    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }