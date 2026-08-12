"""
rootcause_service.py

Performs Root Cause Analysis based on abnormal sensor values.
This module identifies the most probable reason for machine abnormalities.
"""


# Safe Operating Limits

MAX_TEMPERATURE = 70
MAX_VIBRATION = 8
MAX_PRESSURE = 120


def identify_root_cause(temperature, vibration, pressure):

    causes = []

    recommendations = []

    confidence = 0

    # ----------------------------------------
    # Bearing Wear
    # ----------------------------------------

    if temperature > MAX_TEMPERATURE and vibration > MAX_VIBRATION:

        causes.append("Bearing Wear")

        recommendations.append(
            "Inspect and replace machine bearings."
        )

        confidence = max(confidence, 92)

    # ----------------------------------------
    # Cooling System Failure
    # ----------------------------------------

    if temperature > MAX_TEMPERATURE and pressure > MAX_PRESSURE:

        causes.append("Cooling System Failure")

        recommendations.append(
            "Inspect cooling fan, coolant flow and heat exchanger."
        )

        confidence = max(confidence, 90)

    # ----------------------------------------
    # Shaft Misalignment
    # ----------------------------------------

    if vibration > MAX_VIBRATION and pressure <= MAX_PRESSURE:

        causes.append("Shaft Misalignment")

        recommendations.append(
            "Perform shaft alignment and balancing."
        )

        confidence = max(confidence, 87)

    # ----------------------------------------
    # Valve Blockage
    # ----------------------------------------

    if pressure > MAX_PRESSURE and vibration <= MAX_VIBRATION:

        causes.append("Valve Blockage")

        recommendations.append(
            "Inspect valves and clean pressure lines."
        )

        confidence = max(confidence, 88)

    # ----------------------------------------
    # Multiple System Failure
    # ----------------------------------------

    if (
        temperature > MAX_TEMPERATURE
        and vibration > MAX_VIBRATION
        and pressure > MAX_PRESSURE
    ):

        causes = ["Multiple System Failure"]

        recommendations = [
            "Immediate shutdown recommended.",
            "Complete machine inspection required."
        ]

        confidence = 98

    # ----------------------------------------
    # No Issues
    # ----------------------------------------

    if not causes:

        causes.append("No Significant Fault Detected")

        recommendations.append(
            "Continue Normal Machine Operation."
        )

        confidence = 100

    return {

        "root_cause": causes,

        "confidence": f"{confidence}%",

        "recommendations": recommendations

    }