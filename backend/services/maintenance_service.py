"""
maintenance_service.py

Provides intelligent maintenance recommendations
based on machine health score and root cause.
"""

from datetime import datetime, timedelta


def maintenance_recommendation(health_score, root_cause):

    maintenance_type = ""
    priority = ""
    assigned_team = ""
    estimated_duration = ""
    spare_parts = []
    estimated_cost = 0
    next_maintenance = ""
    remarks = ""

    # -----------------------------------------
    # Healthy Machine
    # -----------------------------------------

    if health_score >= 85:

        maintenance_type = "No Maintenance Required"
        priority = "Low"
        assigned_team = "None"
        estimated_duration = "0 Hours"
        spare_parts = []
        estimated_cost = 0
        next_maintenance = (
            datetime.now() + timedelta(days=30)
        ).strftime("%d-%m-%Y")
        remarks = "Machine is operating normally."

    # -----------------------------------------
    # Warning Condition
    # -----------------------------------------

    elif health_score >= 60:

        maintenance_type = "Preventive Maintenance"
        priority = "Medium"
        estimated_duration = "2 Hours"
        estimated_cost = 5000
        next_maintenance = (
            datetime.now() + timedelta(days=7)
        ).strftime("%d-%m-%Y")
        remarks = "Maintenance should be scheduled soon."

    # -----------------------------------------
    # Critical Condition
    # -----------------------------------------

    else:

        maintenance_type = "Corrective Maintenance"
        priority = "High"
        estimated_duration = "4 Hours"
        estimated_cost = 15000
        next_maintenance = "Immediately"
        remarks = "Machine requires immediate attention."

    # -----------------------------------------
    # Decide Team & Spare Parts
    # -----------------------------------------

    if "Bearing Wear" in root_cause:

        assigned_team = "Mechanical Team"

        spare_parts.extend([
            "Bearing Kit",
            "Lubricant"
        ])

    elif "Cooling System Failure" in root_cause:

        assigned_team = "Cooling Team"

        spare_parts.extend([
            "Coolant",
            "Cooling Fan"
        ])

    elif "Valve Blockage" in root_cause:

        assigned_team = "Hydraulic Team"

        spare_parts.extend([
            "Valve Kit",
            "Pressure Seal"
        ])

    elif "Shaft Misalignment" in root_cause:

        assigned_team = "Mechanical Team"

        spare_parts.extend([
            "Alignment Kit"
        ])

    elif "Multiple System Failure" in root_cause:

        assigned_team = "Emergency Maintenance Team"

        spare_parts.extend([
            "Bearing Kit",
            "Cooling Fan",
            "Valve Kit",
            "Lubricant"
        ])

        priority = "Critical"

        estimated_duration = "8 Hours"

        estimated_cost = 50000

    if assigned_team == "":

        assigned_team = "General Maintenance Team"

    # -----------------------------------------
    # Return Report
    # -----------------------------------------

    return {

        "maintenance_type": maintenance_type,

        "priority": priority,

        "assigned_team": assigned_team,

        "estimated_duration": estimated_duration,

        "spare_parts": spare_parts,

        "estimated_cost": f"₹{estimated_cost}",

        "next_maintenance": next_maintenance,

        "remarks": remarks

    }