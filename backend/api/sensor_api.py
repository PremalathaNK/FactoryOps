from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.sensor_crud import (
    get_all_sensor_data,
    get_sensor_data_by_id,
    get_sensor_data_by_machine,
    create_sensor_data
)

from backend.schemas.sensor_schema import (
    SensorCreate,
    SensorResponse
)


router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


# ============================================================
# GET ALL SENSOR DATA
# ============================================================

@router.get(
    "/",
    response_model=List[SensorResponse]
)
def get_sensors(
    db: Session = Depends(get_db)
):
    sensor_data = get_all_sensor_data(db)

    return sensor_data


# ============================================================
# GET SENSOR DATA BY ID
# ============================================================

@router.get(
    "/{sensor_id}",
    response_model=SensorResponse
)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    sensor = get_sensor_data_by_id(
        db,
        sensor_id
    )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor data not found"
        )

    return sensor


# ============================================================
# GET SENSOR DATA FOR A MACHINE
# ============================================================

@router.get(
    "/machine/{machine_id}",
    response_model=List[SensorResponse]
)
def get_machine_sensor_data(
    machine_id: int,
    db: Session = Depends(get_db)
):
    sensor_data = get_sensor_data_by_machine(
        db,
        machine_id
    )

    if not sensor_data:
        raise HTTPException(
            status_code=404,
            detail="No sensor data found for this machine"
        )

    return sensor_data


# ============================================================
# CREATE SENSOR DATA
# ============================================================

@router.post(
    "/",
    response_model=SensorResponse,
    status_code=201
)
def create_new_sensor_data(
    sensor_data: SensorCreate,
    db: Session = Depends(get_db)
):
    return create_sensor_data(
        db,
        sensor_data
    )