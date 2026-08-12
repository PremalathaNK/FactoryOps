"""
health_service.py

This service calculates the overall health of a machine
using temperature, vibration and pressure sensor values.
"""


# -----------------------------
# Safe Operating Limits
# -----------------------------

MAX_TEMPERATURE = 70
MAX_VIBRATION = 8
MAX_PRESSURE = 120


# -----------------------------
# Main Function
# -----------------------------

def calculate_health(temperature, vibration, pressure):

    health_score = 100
    alerts = []

    # -----------------------------
    # Temperature Check
    # -----------------------------
    if temperature > MAX_TEMPERATURE:

        deduction = min((temperature - MAX_TEMPERATURE), 30)

        health_score -= deduction

        alerts.append(
            f"High Temperature ({temperature}°C)"
        )

    # -----------------------------
    # Vibration Check
    # -----------------------------
    if vibration > MAX_VIBRATION:

        deduction = min(
            (vibration - MAX_VIBRATION) * 5,
            35
        )

        health_score -= deduction

        alerts.append(
            f"High Vibration ({vibration} mm/s)"
        )

    # -----------------------------
    # Pressure Check
    # -----------------------------
    if pressure > MAX_PRESSURE:

        deduction = min(
            (pressure - MAX_PRESSURE) // 2,
            25
        )

        health_score -= deduction

        alerts.append(
            f"High Pressure ({pressure} PSI)"
        )

    # -----------------------------
    # Ensure Score Never Goes Below 0
    # -----------------------------

    health_score = max(int(health_score), 0)

    # -----------------------------
    # Machine Status
    # -----------------------------

    if health_score >= 85:

        status = "Healthy"

        color = "Green"

    elif health_score >= 60:

        status = "Warning"

        color = "Orange"

    else:

        status = "Critical"

        color = "Red"

    # -----------------------------
    # Health Index
    # -----------------------------

    health_index = f"{health_score}%"

    # -----------------------------
    # Return Complete Report
    # -----------------------------

    return {

        "health_score": health_score,

        "health_index": health_index,

        "status": status,

        "status_color": color,

        "alerts": alerts,

        "total_alerts": len(alerts)

    }