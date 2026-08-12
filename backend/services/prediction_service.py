"""
prediction_service.py

Master Business Logic Service

Combines all business logic services into
one complete prediction report.
"""

from datetime import datetime
from backend.services.health_service import calculate_health
from backend.services.anamoly import detect_anomalies
from backend.services.rootcause import identify_root_cause
from backend.services.maintenance_service import maintenance_recommendation


def generate_prediction_report(
    machine_id,
    temperature,
    vibration,
    pressure
):

    # -----------------------------------
    # Step 1 : Calculate Health
    # -----------------------------------

    health = calculate_health(
        temperature,
        vibration,
        pressure
    )

    # -----------------------------------
    # Step 2 : Detect Anomalies
    # -----------------------------------

    anomaly = detect_anomalies(
        temperature,
        vibration,
        pressure
    )

    # -----------------------------------
    # Step 3 : Root Cause Analysis
    # -----------------------------------

    rootcause = identify_root_cause(
        temperature,
        vibration,
        pressure
    )

    # -----------------------------------
    # Step 4 : Maintenance Recommendation
    # -----------------------------------

    maintenance = maintenance_recommendation(
        health["health_score"],
        rootcause["root_cause"]
    )

    # -----------------------------------
    # Step 5 : Failure Probability
    # -----------------------------------

    if health["health_score"] >= 85:

        failure_probability = "10%"

        risk = "Low"

    elif health["health_score"] >= 60:

        failure_probability = "45%"

        risk = "Medium"

    else:

        failure_probability = "90%"

        risk = "High"

    # -----------------------------------
    # Step 6 : Remaining Useful Life
    # -----------------------------------

    if health["health_score"] >= 85:

        remaining_life = "180 Days"

    elif health["health_score"] >= 60:

        remaining_life = "60 Days"

    else:

        remaining_life = "15 Days"

    # -----------------------------------
    # Final Report
    # -----------------------------------

    return {

        "machine_id": machine_id,

        "generated_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        "sensor_data": {

            "temperature": temperature,

            "vibration": vibration,

            "pressure": pressure

        },

        "health": health,

        "anomaly": anomaly,

        "root_cause": rootcause,

        "maintenance": maintenance,

        "prediction": {

            "failure_probability": failure_probability,

            "risk_level": risk,

            "remaining_useful_life": remaining_life

        }

    }