"""
incident_crud.py

CRUD operations for machine incidents.
"""

from sqlalchemy.orm import Session

from backend.models.incident import Incident


# ============================================================
# GET ALL INCIDENTS
# ============================================================

def get_all_incidents(db: Session):

    return (
        db.query(Incident)
        .order_by(Incident.reported_time.desc())
        .all()
    )


# ============================================================
# GET INCIDENT BY ID
# ============================================================

def get_incident_by_id(
    db: Session,
    incident_id: int
):

    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


# ============================================================
# GET INCIDENTS FOR A MACHINE
# ============================================================

def get_incidents_by_machine(
    db: Session,
    machine_id: int
):

    return (
        db.query(Incident)
        .filter(Incident.machine_id == machine_id)
        .order_by(Incident.reported_time.desc())
        .all()
    )