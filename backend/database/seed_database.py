"""
seed_database.py

Generates realistic factory data for testing.

Creates:
- Machines
- Sensors
- Predictions
- Maintenance Records
- Incidents

Run:
python backend/database/seed_database.py
"""

import random
from datetime import datetime, timedelta

from faker import Faker

from backend.db_config import Base, engine, SessionLocal

from backend.models.machine import Machine
from backend.models.sensor import Sensor
from backend.models.prediction import Prediction
from backend.models.maintenance import Maintenance
from backend.models.incident import Incident

from backend.services.health_service import calculate_health
from backend.services.anamoly import detect_anomalies
from backend.services.prediction_service import generate_prediction_report
from backend.services.maintenance_service import maintenance_recommendation
from backend.services.rootcause import identify_root_cause


fake = Faker()

# Create all database tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()



# =====================================================
# FACTORY MASTER DATA
# =====================================================

MACHINE_TYPES = [

    "CNC Machine",
    "Hydraulic Press",
    "Lathe Machine",
    "Conveyor Belt",
    "Boiler",
    "Air Compressor",
    "Packing Machine",
    "Grinding Machine",
    "Injection Molding Machine",
    "Robotic Arm"

]

DEPARTMENTS = [

    "Production",
    "Assembly",
    "Packaging",
    "Maintenance",
    "Utilities",
    "Warehouse",
    "Quality Control"

]

ENGINEERS = [

    "John Smith",
    "David Wilson",
    "Emily Johnson",
    "Sophia Davis",
    "Michael Brown",
    "Olivia Taylor",
    "Daniel Harris",
    "James Anderson"

]


# =====================================================
# CREATE MACHINES
# =====================================================

def create_machines():

    print("Creating Machines...")

    machines = []

    for i in range(1, 101):

        machine = Machine(

            machine_code=f"MC-{1000+i}",

            machine_name=f"{random.choice(MACHINE_TYPES)} {i}",

            machine_type=random.choice(MACHINE_TYPES),

            department=random.choice(DEPARTMENTS),

            installation_date=fake.date_time_between(
                start_date="-6y",
                end_date="-2y"
            ),

            operating_hours=random.randint(1000, 20000),

            health_status="Healthy",

            last_service_date=fake.date_time_between(
                start_date="-8m",
                end_date="-10d"
            )

        )

        db.add(machine)

        machines.append(machine)

    db.commit()

    for machine in machines:

        db.refresh(machine)

    print(f"{len(machines)} Machines Created")

    return machines

# =====================================================
# GENERATE SENSOR DATA
# =====================================================

def generate_sensor_data(machines):

    print("Generating Sensor Data...")

    for machine in machines:

        for reading in range(10):

            # -------------------------------------
            # Generate Realistic Sensor Values
            # -------------------------------------

            temperature = round(random.uniform(45, 95), 2)

            vibration = round(random.uniform(2, 14), 2)

            pressure = round(random.uniform(80, 150), 2)

            humidity = round(random.uniform(40, 85), 2)

            voltage = round(random.uniform(210, 245), 2)

            current = round(random.uniform(10, 60), 2)

            sensor = Sensor(

                machine_id=machine.id,

                temperature=temperature,

                vibration=vibration,

                pressure=pressure,

                humidity=humidity,

                voltage=voltage,

                current=current,

                timestamp=datetime.utcnow()

            )

            db.add(sensor)

            # -------------------------------------
            # BUSINESS LOGIC
            # -------------------------------------

            health = calculate_health(

                temperature,

                vibration,

                pressure

            )

            anomaly = detect_anomalies(

                temperature,

                vibration,

                pressure

            )

            rootcause = identify_root_cause(

                temperature,

                vibration,

                pressure

            )

            maintenance = maintenance_recommendation(

                health["health_score"],

                rootcause["root_cause"]

            )

            report = generate_prediction_report(

                machine.id,

                temperature,

                vibration,

                pressure

            )

            # Only create prediction once per machine
            if reading == 9:

                create_prediction(

                    machine,

                    health,

                    report

                )

                create_maintenance(

                    machine,

                    maintenance

                )

                create_incident(

                    machine,

                    anomaly,

                    rootcause

                )

    db.commit()

    print("1000 Sensor Records Generated")

    # =====================================================
# CREATE PREDICTION RECORD
# =====================================================

def create_prediction(machine, health, report):

    prediction = Prediction(

        machine_id=machine.id,

        health_score=health["health_score"],

        failure_probability=float(
            report["prediction"]["failure_probability"].replace("%", "")
        ),

        risk_level=report["prediction"]["risk_level"],

        predicted_failure=report["root_cause"]["root_cause"][0],

        estimated_failure_days=int(
            report["prediction"]["remaining_useful_life"].split()[0]
        ),

        confidence_score=float(
            report["root_cause"]["confidence"].replace("%", "")
        )

    )

    db.add(prediction)


# =====================================================
# CREATE MAINTENANCE RECORD
# =====================================================

def create_maintenance(machine, maintenance):

    if maintenance["next_maintenance"] == "Immediately":

        scheduled = datetime.utcnow()

    else:

        scheduled = datetime.strptime(

            maintenance["next_maintenance"],

            "%d-%m-%Y"

        )

    record = Maintenance(

        machine_id=machine.id,

        maintenance_type=maintenance["maintenance_type"],

        priority=maintenance["priority"],

        engineer=random.choice(ENGINEERS),

        scheduled_date=scheduled,

        completion_status=random.choice(

            [

                "Pending",

                "Scheduled",

                "Completed"

            ]

        ),

        remarks=maintenance["remarks"]

    )

    db.add(record)


# =====================================================
# CREATE INCIDENT RECORD
# =====================================================

def create_incident(machine, anomaly, rootcause):

    # Don't create incidents for healthy machines

    if not anomaly["anomaly_detected"]:

        return

    incident = Incident(

        machine_id=machine.id,

        incident_type="Machine Abnormality",

        severity=anomaly["severity"],

        root_cause=", ".join(rootcause["root_cause"]),

        description="Sensor values exceeded operating limits.",

        action_taken=rootcause["recommendations"][0],

        resolved_status=random.choice(

            [

                "Pending",

                "Resolved",

                "Under Investigation"

            ]

        )

    )

    db.add(incident)

    # =====================================================
# MAIN FUNCTION
# =====================================================

def seed_database():

    print("\n======================================")
    print(" PREDICTIVE MAINTENANCE DATABASE SEED ")
    print("======================================\n")

    # Step 1
    machines = create_machines()

    # Step 2
    generate_sensor_data(machines)

    print("\n======================================")
    print(" DATABASE SEEDED SUCCESSFULLY ")
    print("======================================")

    print("\nSummary")
    print("----------------------------")
    print(f"Machines Created      : {len(machines)}")
    print("Sensor Records        : 1000")
    print("Prediction Records    : 100")
    print("Maintenance Records   : 100")
    print("Incidents             : Auto Generated")
    print("----------------------------")

    db.close()


# =====================================================
# RUN SCRIPT
# =====================================================

if __name__ == "__main__":

    seed_database()