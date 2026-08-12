from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from backend.database import Base


class Machine(Base):

    __tablename__ = "machines"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    machine_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    machine_name = Column(
        String(100),
        nullable=False
    )

    machine_type = Column(
        String(50),
        nullable=False
    )

    department = Column(
        String(50),
        nullable=False
    )

    installation_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    operating_hours = Column(
        Float,
        default=0
    )

    health_status = Column(
        String(20),
        default="Healthy"
    )

    last_service_date = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )