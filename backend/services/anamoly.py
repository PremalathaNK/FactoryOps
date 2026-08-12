"""
anomaly_service.py

Detects abnormal sensor behaviour in a machine.
Returns anomaly status, severity, affected sensors,
and recommended actions.
"""


# Safe Operating Limits

MAX_TEMPERATURE = 70
MAX_VIBRATION = 8
MAX_PRESSURE = 120


def detect_anomalies(temperature, vibration, pressure):

    anomalies = []

    severity_score = 0

    # -----------------------------
    # Temperature
    # -----------------------------

    if temperature > MAX_TEMPERATURE:

        anomalies.append({
            "sensor": "Temperature",
            "value": temperature,
            "limit": MAX_TEMPERATURE,
            "message": "Temperature exceeded safe limit"
        })

        severity_score += 2

    # -----------------------------
    # Vibration
    # -----------------------------

    if vibration > MAX_VIBRATION:

        anomalies.append({
            "sensor": "Vibration",
            "value": vibration,
            "limit": MAX_VIBRATION,
            "message": "Excessive machine vibration detected"
        })

        severity_score += 3

    # -----------------------------
    # Pressure
    # -----------------------------

    if pressure > MAX_PRESSURE:

        anomalies.append({
            "sensor": "Pressure",
            "value": pressure,
            "limit": MAX_PRESSURE,
            "message": "Pressure crossed operating limit"
        })

        severity_score += 2

    # -----------------------------
    # Overall Severity
    # -----------------------------

    if severity_score == 0:

        severity = "None"

        action = "Machine Operating Normally"

    elif severity_score <= 2:

        severity = "Low"

        action = "Continue Monitoring"

    elif severity_score <= 5:

        severity = "Medium"

        action = "Schedule Inspection"

    else:

        severity = "High"

        action = "Immediate Shutdown Recommended"

    return {

        "anomaly_detected": severity_score > 0,

        "severity": severity,

        "severity_score": severity_score,

        "affected_sensors": len(anomalies),

        "recommended_action": action,

        "anomalies": anomalies

    }