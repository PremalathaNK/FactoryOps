"""
prediction_schema.py

Schema for returning AI prediction results.
"""

from pydantic import BaseModel


class PredictionResponse(BaseModel):

    machine_id: int

    health_score: float

    failure_probability: float

    risk_level: str

    predicted_failure: str

    estimated_failure_days: int

    confidence_score: float

    class Config:

        from_attributes = True