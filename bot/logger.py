import datetime
import os


def log(text: str, level: str = "INFO"):
    current_time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    print(text)

    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, "bot_reservas")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    log_path = os.path.join(folder_path, "log.txt")
    with open(log_path, "a") as file:
        file.write(f"[{current_time} - {level}]: {text}\n")

