"""
incident_api.py

API endpoints for machine failure incidents.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.incident_crud import (
    get_all_incidents,
    get_incidents_by_machine,
    get_incident_by_id
)

from backend.schemas.incident_schema import IncidentResponse


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


# ============================================================
# GET ALL INCIDENTS
# ============================================================

@router.get(
    "/",
    response_model=List[IncidentResponse]
)
def get_incidents(
    db: Session = Depends(get_db)
):

    incidents = get_all_incidents(db)

    return incidents


# ============================================================
# GET INCIDENTS FOR A MACHINE
# ============================================================

@router.get(
    "/machine/{machine_id}",
    response_model=List[IncidentResponse]
)
def get_machine_incidents(
    machine_id: int,
    db: Session = Depends(get_db)
):

    incidents = get_incidents_by_machine(
        db,
        machine_id
    )

    if not incidents:

        raise HTTPException(
            status_code=404,
            detail="No incidents found for this machine"
        )

    return incidents


# ============================================================
# GET INCIDENT BY ID
# ============================================================

@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):

    incident = get_incident_by_id(
        db,
        incident_id
    )

    if incident is None:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident