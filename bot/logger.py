import datetime
import os


def log(text: str, level: str = "INFO"):
    print(text)

    home_dir = os.path.expanduser("~")
    program_folder = os.path.join(home_dir, "bot_reservas")

    if not os.path.exists(program_folder):
        os.makedirs(program_folder)

    log_file = os.path.join(program_folder, "log.txt")
    with open(log_file, "a") as file:
        current_time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        file.write(f"[{current_time} - {level}]: {text}\n")
