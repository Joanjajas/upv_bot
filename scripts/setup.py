import platform
import shutil
import os
import subprocess

from get_credentials import get_credentials


def main():
    install_deps()
    username, password = get_credentials()
    install_script()


def install_deps():
    print("Installing dependencies...")

    if platform.system() == "Darwin":
        run_command(["/usr/bin/python3", "-m", "pip", "install", "toml"])
        run_command(["/usr/bin/python3", "-m", "pip", "install", "dsfdsfdsf"])
        run_command(["/usr/bin/python3", "-m", "playwright", "install", "chromium"])

    if platform.system() == "Windows":
        run_command(["pip", "install", "toml"])
        run_command(["pip", "install", "playwright"])
        run_command(["python", "-m", "playwright", "install", "chromium"])


def run_command(command):
    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    except Exception as err:
        print("Error running command: ", err)
        exit(1)


def install_script():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    if platform.system() == "Darwin":
        install_dir = "/usr/local/reservation_bot"

        if os.path.exists(install_dir):
            run_command(["sudo", "rm", "-rf", install_dir])

        run_command(["sudo", "cp", "-r", f"{root_dir}/bot", install_dir])

    if platform.system() == "Windows":
        install_dir = "C:\\Program Files (x86)\\reservation_bot"

        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)

        shutil.copytree(f"{root_dir}\\bot", install_dir)


if __name__ == "__main__":
    main()
