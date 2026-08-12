"""
prediction_api.py

API endpoints for machine health and failure predictions.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.prediction_crud import (
    get_all_predictions,
    get_prediction_by_id,
    get_predictions_by_machine
)

from backend.schemas.prediction_schema import (
    PredictionResponse
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


# ============================================================
# GET ALL PREDICTIONS
# ============================================================

@router.get(
    "/",
    response_model=List[PredictionResponse]
)
def get_predictions(
    db: Session = Depends(get_db)
):

    predictions = get_all_predictions(
        db
    )

    return predictions


# ============================================================
# GET PREDICTION BY ID
# ============================================================

@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse
)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):

    prediction = get_prediction_by_id(
        db,
        prediction_id
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return prediction


# ============================================================
# GET PREDICTIONS FOR A MACHINE
# ============================================================

@router.get(
    "/machine/{machine_id}",
    response_model=List[PredictionResponse]
)
def get_machine_predictions(
    machine_id: int,
    db: Session = Depends(get_db)
):

    predictions = get_predictions_by_machine(
        db,
        machine_id
    )

    if not predictions:

        raise HTTPException(
            status_code=404,
            detail="No sensor data found for this machine"
        )

    return predictions