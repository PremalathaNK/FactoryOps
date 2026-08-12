from datetime import datetime


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")