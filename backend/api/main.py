from fastapi import FastAPI
from sqlalchemy import text

from backend.config import settings

from backend.database import (
    Base,
    engine,
    SessionLocal
)

# ============================================================
# IMPORT ALL DATABASE MODELS
# ============================================================

from backend.models.machine import Machine
from backend.models.sensor import Sensor
from backend.models.prediction import Prediction
from backend.models.maintenance import Maintenance
from backend.models.incident import Incident

# ============================================================
# IMPORT API ROUTERS
# ============================================================

from backend.api.machine_api import router as machine_router
from backend.api.sensor_api import router as sensor_router
from backend.api.prediction_api import router as prediction_router
from backend.api.maintenance_api import router as maintenance_router
from backend.api.incident_api import router as incident_router
from backend.api.dashboard_api import router as dashboard_router

# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    description="""
Smart Factory Predictive Maintenance
and Process Intelligence System.

This backend provides APIs for:

• Machine Monitoring
• Sensor Data Collection
• Health Score Analysis
• Failure Prediction
• Maintenance Recommendations
• Incident Management
• Dashboard Analytics
""",
    version=settings.APP_VERSION
)

# ============================================================
# HOME
# ============================================================

@app.get(
    "/",
    tags=["Home"]
)
def home():

    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running",
        "message": "Welcome to the Smart Factory Predictive Maintenance Backend"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["System"]
)
def health():

    db = SessionLocal()

    try:

        db.execute(
            text("SELECT 1")
        )

        database_status = "Connected"

    except Exception:

        database_status = "Disconnected"

    finally:

        db.close()

    return {
        "application": "Healthy",
        "database": database_status,
        "server": "Running"
    }


# ============================================================
# MACHINE API
# ============================================================

app.include_router(
    machine_router
)

# ============================================================
# SENSOR API
# ============================================================

app.include_router(
    sensor_router
)

# ============================================================
# PREDICTION API
# ============================================================

app.include_router(
    prediction_router
)

# ============================================================
# MAINTENANCE API
# ============================================================

app.include_router(
    maintenance_router
)

# ============================================================
# INCIDENT API
# ============================================================

app.include_router(
    incident_router
)

# ============================================================
# DASHBOARD API
# ============================================================

app.include_router(
    dashboard_router
)