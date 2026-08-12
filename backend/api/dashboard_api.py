"""
dashboard_api.py

API endpoint for factory dashboard summary.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud.prediction_crud import calculate_prediction

from backend.services.maintenance_service import (
    maintenance_recommendation
)

from backend.services.dashboard_service import (
    get_dashboard_summary
)

from backend.models.machine import Machine
from backend.models.sensor import Sensor


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    machines = (
        db.query(Machine)
        .order_by(Machine.id)
        .all()
    )

    machine_reports = []

    for machine in machines:

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = calculate_prediction(
            db,
            machine.id
        )

        if prediction is None:
            continue

        # ----------------------------------------------------
        # Latest sensor
        # ----------------------------------------------------

        sensor = (
            db.query(Sensor)
            .filter(
                Sensor.machine_id == machine.id
            )
            .order_by(
                Sensor.timestamp.desc()
            )
            .first()
        )

        if sensor is None:
            continue

        # ----------------------------------------------------
        # Convert prediction risk to dashboard status
        # ----------------------------------------------------

        risk_level = prediction["risk_level"]

        if risk_level == "Low":
            status = "Healthy"

        elif risk_level == "Medium":
            status = "Warning"

        else:
            status = "Critical"

        # ----------------------------------------------------
        # Alerts
        #
        # Count the sensor abnormalities that contributed
        # to the prediction.
        # ----------------------------------------------------

        total_alerts = 0

        sensor_values = [
            sensor.temperature,
            sensor.vibration,
            sensor.pressure,
            sensor.humidity,
            sensor.voltage,
            sensor.current
        ]

        # Count abnormal sensor values using the prediction
        # failure probability as an indication that at least
        # one condition is abnormal.
        #
        # A completely normal machine has zero alerts.
        if prediction["failure_probability"] > 0:
            total_alerts = 1

        # ----------------------------------------------------
        # Health object
        # ----------------------------------------------------

        health = {
            "health_score": prediction["health_score"],
            "status": status,
            "total_alerts": total_alerts
        }

        # ----------------------------------------------------
        # Root cause
        # ----------------------------------------------------

        root_cause = prediction.get(
            "predicted_failure",
            "Unknown"
        )

        # ----------------------------------------------------
        # Maintenance
        # ----------------------------------------------------

        maintenance = maintenance_recommendation(
            prediction["health_score"],
            root_cause
        )

        # ----------------------------------------------------
        # Machine report
        # ----------------------------------------------------

        machine_report = {

            "machine_id": machine.id,

            "machine_code": machine.machine_code,

            "machine_name": machine.machine_name,

            "health": health,

            "prediction": prediction,

            "maintenance": maintenance

        }

        machine_reports.append(
            machine_report
        )

    # --------------------------------------------------------
    # Dashboard summary
    # --------------------------------------------------------

    return get_dashboard_summary(
        machine_reports
    )