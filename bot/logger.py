import datetime
import os


def log(text: str, level: str = "INFO"):
    current_time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    print(f"[{current_time} - {level}]: {text}")


def create_log_file(filename: str):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")
