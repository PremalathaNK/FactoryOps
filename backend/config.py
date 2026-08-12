import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Smart Factory Predictive Maintenance API"
    APP_VERSION = "1.0"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./factoryops.db"
    )

    HEALTH_THRESHOLD = 70
    CRITICAL_THRESHOLD = 40

settings = Settings()