"""
dashboard_service.py

Creates a dashboard summary for the factory
using prediction reports of all machines.
"""


def get_dashboard_summary(machine_reports):

    total_machines = len(machine_reports)

    healthy = 0
    warning = 0
    critical = 0

    total_health = 0

    maintenance_due = 0

    active_alerts = 0

    high_risk = 0

    for report in machine_reports:

        health = report["health"]["health_score"]

        total_health += health

        status = report["health"]["status"]

        if status == "Healthy":

            healthy += 1

        elif status == "Warning":

            warning += 1

        else:

            critical += 1

        active_alerts += report["health"]["total_alerts"]

        if report["maintenance"]["priority"] in ["High", "Critical"]:

            maintenance_due += 1

        if report["prediction"]["risk_level"] == "High":

            high_risk += 1

    # ---------------------------------------
    # Average Health
    # ---------------------------------------

    average_health = (
        total_health / total_machines
        if total_machines > 0
        else 0
    )

    # ---------------------------------------
    # Overall Factory Status
    # ---------------------------------------

    if critical > 0:

        factory_status = "Critical"

    elif warning > 0:

        factory_status = "Warning"

    else:

        factory_status = "Healthy"

    # ---------------------------------------
    # Machine Availability
    # ---------------------------------------

    machine_availability = (
        round(
            (healthy + warning) / total_machines * 100,
            2
        )
        if total_machines > 0
        else 0
    )

    # ---------------------------------------
    # Final Dashboard Summary
    # ---------------------------------------

    return {

        "factory_status": factory_status,

        "total_machines": total_machines,

        "healthy_machines": healthy,

        "warning_machines": warning,

        "critical_machines": critical,

        "average_health_score": round(
            average_health,
            2
        ),

        "machine_availability": f"{machine_availability}%",

        "active_alerts": active_alerts,

        "maintenance_due": maintenance_due,

        "high_failure_risk": high_risk

    }