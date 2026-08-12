from sqlalchemy.orm import Session

from backend.models.sensor import Sensor
from backend.schemas.sensor_schema import SensorCreate


def get_all_sensor_data(db: Session):
    return (
        db.query(Sensor)
        .order_by(Sensor.timestamp.desc())
        .all()
    )


def get_sensor_data_by_id(
    db: Session,
    sensor_id: int
):
    return (
        db.query(Sensor)
        .filter(Sensor.id == sensor_id)
        .first()
    )


def get_sensor_data_by_machine(
    db: Session,
    machine_id: int
):
    return (
        db.query(Sensor)
        .filter(Sensor.machine_id == machine_id)
        .order_by(Sensor.timestamp.desc())
        .all()
    )


def create_sensor_data(
    db: Session,
    sensor_data: SensorCreate
):
    sensor = Sensor(
        machine_id=sensor_data.machine_id,
        temperature=sensor_data.temperature,
        vibration=sensor_data.vibration,
        pressure=sensor_data.pressure,
        humidity=sensor_data.humidity,
        voltage=sensor_data.voltage,
        current=sensor_data.current
    )

    db.add(sensor)
    db.commit()
    db.refresh(sensor)

    return sensor