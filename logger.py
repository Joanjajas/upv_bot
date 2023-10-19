import datetime


def log(text: str, level: str = "INFO"):
    current_time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    print(f"[{current_time} - {level}]: {text}")
