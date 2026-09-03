from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.machine_crud import (
    get_all_machines,
    get_machine_by_id,
    get_machine_by_code,
    create_machine
)
from backend.crud.prediction_crud import calculate_prediction

from backend.schemas.machine_schema import (
    MachineCreate,
    MachineResponse
)


router = APIRouter(
    prefix="/machines",
    tags=["Machines"]
)


def apply_current_health_status(db: Session, machine):

    prediction = calculate_prediction(
        db,
        machine.id
    )

    if prediction is None:
        machine.health_status = "Unknown"
    else:
        machine.health_status = {
            "Low": "Healthy",
            "Medium": "Warning",
            "High": "Critical",
        }.get(
            prediction["risk_level"],
            "Unknown"
        )

    return machine


@router.get(
    "/",
    response_model=List[MachineResponse]
)
def get_machines(
    db: Session = Depends(get_db)
):

    machines = get_all_machines(db)

    return [
        apply_current_health_status(db, machine)
        for machine in machines
    ]


@router.get(
    "/{machine_id}",
    response_model=MachineResponse
)
def get_machine(
    machine_id: int,
    db: Session = Depends(get_db)
):

    machine = get_machine_by_id(
        db,
        machine_id
    )

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return apply_current_health_status(db, machine)


@router.get(
    "/code/{machine_code}",
    response_model=MachineResponse
)
def get_machine_by_code_endpoint(
    machine_code: str,
    db: Session = Depends(get_db)
):

    machine = get_machine_by_code(
        db,
        machine_code
    )

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return machine


@router.post(
    "/",
    response_model=MachineResponse,
    status_code=201
)
def create_new_machine(
    machine_data: MachineCreate,
    db: Session = Depends(get_db)
):

    existing_machine = get_machine_by_code(
        db,
        machine_data.machine_code
    )

    if existing_machine is not None:

        raise HTTPException(
            status_code=400,
            detail="Machine code already exists"
        )

    return create_machine(
        db,
        machine_data
    )