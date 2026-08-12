from sqlalchemy.orm import Session

from backend.models.machine import Machine
from backend.schemas.machine_schema import MachineCreate


def get_all_machines(db: Session):

    return (
        db.query(Machine)
        .order_by(Machine.id)
        .all()
    )


def get_machine_by_id(
    db: Session,
    machine_id: int
):

    return (
        db.query(Machine)
        .filter(Machine.id == machine_id)
        .first()
    )


def get_machine_by_code(
    db: Session,
    machine_code: str
):

    return (
        db.query(Machine)
        .filter(Machine.machine_code == machine_code)
        .first()
    )


def create_machine(
    db: Session,
    machine_data: MachineCreate
):

    machine = Machine(
        machine_code=machine_data.machine_code,
        machine_name=machine_data.machine_name,
        machine_type=machine_data.machine_type,
        department=machine_data.department,
        installation_date=machine_data.installation_date,
        operating_hours=machine_data.operating_hours,
        health_status=machine_data.health_status,
        last_service_date=machine_data.last_service_date
    )

    db.add(machine)
    db.commit()
    db.refresh(machine)

    return machine