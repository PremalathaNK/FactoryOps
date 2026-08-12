"""
maintenance_api.py

API endpoints for maintenance records.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.maintenance_crud import (
    get_all_maintenance,
    get_maintenance_by_id,
    get_maintenance_by_machine
)

from backend.schemas.maintenance_schema import (
    MaintenanceResponse
)


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


# ============================================================
# GET ALL MAINTENANCE RECORDS
# ============================================================

@router.get(
    "/",
    response_model=List[MaintenanceResponse]
)
def get_maintenance_records(
    db: Session = Depends(get_db)
):

    maintenance_records = get_all_maintenance(db)

    return maintenance_records


# ============================================================
# GET MAINTENANCE FOR A MACHINE
# ============================================================

@router.get(
    "/machine/{machine_id}",
    response_model=List[MaintenanceResponse]
)
def get_machine_maintenance(
    machine_id: int,
    db: Session = Depends(get_db)
):

    maintenance_records = get_maintenance_by_machine(
        db,
        machine_id
    )

    if not maintenance_records:

        raise HTTPException(
            status_code=404,
            detail="No maintenance records found for this machine"
        )

    return maintenance_records


# ============================================================
# GET MAINTENANCE BY ID
# ============================================================

@router.get(
    "/{maintenance_id}",
    response_model=MaintenanceResponse
)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    maintenance = get_maintenance_by_id(
        db,
        maintenance_id
    )

    if maintenance is None:

        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return maintenance