"""
prediction_crud.py

Handles prediction calculations using the latest
sensor readings for each machine.
"""

from sqlalchemy.orm import Session

from backend.models.sensor import Sensor


# ============================================================
# SENSOR LIMITS
# ============================================================

TEMPERATURE_NORMAL_MAX = 75
TEMPERATURE_WARNING_MAX = 85

VIBRATION_NORMAL_MAX = 5
VIBRATION_WARNING_MAX = 10

PRESSURE_NORMAL_MIN = 90
PRESSURE_NORMAL_MAX = 110
PRESSURE_WARNING_MIN = 80
PRESSURE_WARNING_MAX = 120

HUMIDITY_NORMAL_MIN = 30
HUMIDITY_NORMAL_MAX = 70
HUMIDITY_WARNING_MIN = 20
HUMIDITY_WARNING_MAX = 80

VOLTAGE_NORMAL_MIN = 220
VOLTAGE_NORMAL_MAX = 240
VOLTAGE_WARNING_MIN = 210
VOLTAGE_WARNING_MAX = 250

CURRENT_NORMAL_MIN = 10
CURRENT_NORMAL_MAX = 30
CURRENT_WARNING_MIN = 5
CURRENT_WARNING_MAX = 35


# ============================================================
# LATEST SENSOR DATA
# ============================================================

def get_latest_sensor_data_for_machine(
    db: Session,
    machine_id: int
):
    return (
        db.query(Sensor)
        .filter(Sensor.machine_id == machine_id)
        .order_by(Sensor.timestamp.desc())
        .first()
    )


# ============================================================
# TEMPERATURE ANALYSIS
# ============================================================

def analyze_temperature(value: float):

    if value <= TEMPERATURE_NORMAL_MAX:
        return 0, "Normal"

    if value <= TEMPERATURE_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# VIBRATION ANALYSIS
# ============================================================

def analyze_vibration(value: float):

    if value <= VIBRATION_NORMAL_MAX:
        return 0, "Normal"

    if value <= VIBRATION_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# PRESSURE ANALYSIS
# ============================================================

def analyze_pressure(value: float):

    if PRESSURE_NORMAL_MIN <= value <= PRESSURE_NORMAL_MAX:
        return 0, "Normal"

    if PRESSURE_WARNING_MIN <= value <= PRESSURE_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# HUMIDITY ANALYSIS
# ============================================================

def analyze_humidity(value: float):

    if HUMIDITY_NORMAL_MIN <= value <= HUMIDITY_NORMAL_MAX:
        return 0, "Normal"

    if HUMIDITY_WARNING_MIN <= value <= HUMIDITY_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# VOLTAGE ANALYSIS
# ============================================================

def analyze_voltage(value: float):

    if VOLTAGE_NORMAL_MIN <= value <= VOLTAGE_NORMAL_MAX:
        return 0, "Normal"

    if VOLTAGE_WARNING_MIN <= value <= VOLTAGE_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# CURRENT ANALYSIS
# ============================================================

def analyze_current(value: float):

    if CURRENT_NORMAL_MIN <= value <= CURRENT_NORMAL_MAX:
        return 0, "Normal"

    if CURRENT_WARNING_MIN <= value <= CURRENT_WARNING_MAX:
        return 1, "Warning"

    return 2, "Critical"


# ============================================================
# CALCULATE PREDICTION
# ============================================================

def calculate_prediction(
    db: Session,
    machine_id: int
):

    sensor = get_latest_sensor_data_for_machine(
        db,
        machine_id
    )

    if sensor is None:
        return None

    # --------------------------------------------------------
    # Analyze every sensor
    # --------------------------------------------------------

    temperature_score, temperature_status = analyze_temperature(
        sensor.temperature
    )

    vibration_score, vibration_status = analyze_vibration(
        sensor.vibration
    )

    pressure_score, pressure_status = analyze_pressure(
        sensor.pressure
    )

    humidity_score, humidity_status = analyze_humidity(
        sensor.humidity
    )

    voltage_score, voltage_status = analyze_voltage(
        sensor.voltage
    )

    current_score, current_status = analyze_current(
        sensor.current
    )

    # --------------------------------------------------------
    # Total sensor risk
    # --------------------------------------------------------

    total_risk = (
        temperature_score
        + vibration_score
        + pressure_score
        + humidity_score
        + voltage_score
        + current_score
    )

    # Maximum possible score = 12
    #
    # 0 - 2   = Low
    # 3 - 5   = Medium
    # 6+      = High
    # --------------------------------------------------------

    health_score = max(
        0,
        round(100 - (total_risk / 12) * 100)
    )

    failure_probability = min(
        100,
        round((total_risk / 12) * 100)
    )

    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if total_risk <= 2:

        risk_level = "Low"

    elif total_risk <= 5:

        risk_level = "Medium"

    else:

        risk_level = "High"

    # --------------------------------------------------------
    # Determine most significant problem
    # --------------------------------------------------------

    sensor_statuses = {
        "Temperature": temperature_score,
        "Vibration": vibration_score,
        "Pressure": pressure_score,
        "Humidity": humidity_score,
        "Voltage": voltage_score,
        "Current": current_score
    }

    highest_sensor_score = max(
        sensor_statuses.values()
    )

    # --------------------------------------------------------
    # Predicted failure
    # --------------------------------------------------------

    if highest_sensor_score == 0:

        predicted_failure = "No Significant Fault Detected"

    else:

        # Find all sensors with the highest severity.
        # This avoids relying directly on max() when
        # multiple sensors have the same score.
        highest_sensors = [
            sensor_name
            for sensor_name, score in sensor_statuses.items()
            if score == highest_sensor_score
        ]

        highest_sensor = highest_sensors[0]

        if highest_sensor == "Temperature":

            predicted_failure = "Overheating Risk"

        elif highest_sensor == "Vibration":

            predicted_failure = "Mechanical Wear"

        elif highest_sensor == "Pressure":

            predicted_failure = "Pressure Anomaly"

        elif highest_sensor == "Humidity":

            predicted_failure = "Humidity Anomaly"

        elif highest_sensor == "Voltage":

            predicted_failure = "Electrical Voltage Anomaly"

        elif highest_sensor == "Current":

            predicted_failure = "Electrical Current Anomaly"

        else:

            predicted_failure = "Sensor Anomaly"

    # --------------------------------------------------------
    # Estimated failure time
    # --------------------------------------------------------

    if risk_level == "Low":

        estimated_failure_days = 90

    elif risk_level == "Medium":

        estimated_failure_days = 30

    else:

        estimated_failure_days = 7

    # --------------------------------------------------------
    # Confidence
    #
    # Confidence represents completeness of the six
    # sensor readings, not ML model accuracy.
    # --------------------------------------------------------

    sensor_values = [
        sensor.temperature,
        sensor.vibration,
        sensor.pressure,
        sensor.humidity,
        sensor.voltage,
        sensor.current
    ]

    available_values = sum(
        value is not None
        for value in sensor_values
    )

    confidence_score = round(
        (available_values / 6) * 100
    )

    # --------------------------------------------------------
    # Return prediction
    # --------------------------------------------------------

    return {
        "machine_id": machine_id,
        "health_score": float(health_score),
        "failure_probability": float(failure_probability),
        "risk_level": risk_level,
        "predicted_failure": predicted_failure,
        "estimated_failure_days": estimated_failure_days,
        "confidence_score": float(confidence_score)
    }


# ============================================================
# GET ALL PREDICTIONS
# ============================================================

def get_all_predictions(db: Session):

    machine_ids = (
        db.query(Sensor.machine_id)
        .distinct()
        .all()
    )

    predictions = []

    for row in machine_ids:

        machine_id = row[0]

        prediction = calculate_prediction(
            db,
            machine_id
        )

        if prediction is not None:
            predictions.append(prediction)

    return predictions


# ============================================================
# GET PREDICTION BY ID
# ============================================================

def get_prediction_by_id(
    db: Session,
    prediction_id: int
):

    # The old stored prediction table is still supported here.
    # This endpoint retrieves the stored record by its database ID.

    from backend.models.prediction import Prediction

    return (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )


# ============================================================
# GET PREDICTIONS BY MACHINE
# ============================================================

def get_predictions_by_machine(
    db: Session,
    machine_id: int
):

    prediction = calculate_prediction(
        db,
        machine_id
    )

    if prediction is None:
        return []

    return [prediction]