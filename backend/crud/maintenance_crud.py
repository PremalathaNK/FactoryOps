"""
maintenance_crud.py

Database operations for maintenance records.
"""

from sqlalchemy.orm import Session

from backend.models.maintenance import Maintenance


# ============================================================
# GET ALL MAINTENANCE RECORDS
# ============================================================

def get_all_maintenance(db: Session):

    return (
        db.query(Maintenance)
        .order_by(Maintenance.created_at.desc())
        .all()
    )


# ============================================================
# GET MAINTENANCE BY ID
# ============================================================

def get_maintenance_by_id(
    db: Session,
    maintenance_id: int
):

    return (
        db.query(Maintenance)
        .filter(
            Maintenance.id == maintenance_id
        )
        .first()
    )


# ============================================================
# GET MAINTENANCE FOR A MACHINE
# ============================================================

def get_maintenance_by_machine(
    db: Session,
    machine_id: int
):

    return (
        db.query(Maintenance)
        .filter(
            Maintenance.machine_id == machine_id
        )
        .order_by(
            Maintenance.created_at.desc()
        )
        .all()
    )