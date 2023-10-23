import platform
import shutil
import os
import subprocess
from getpass import getpass

from playwright.sync_api import sync_playwright

UPV_LOGIN_URL = "https://intranet.upv.es"


def main():
    install_deps()
    get_credentials()
    install_script()


def install_deps():
    print("Installing dependencies...")

    if platform.system() == "Darwin":
        try:
            run_command(["/usr/bin/python3", "-m", "pip", "install", "toml"])
            run_command(["/usr/bin/python3", "-m", "pip", "install", "playwright"])
            run_command(["/usr/bin/python3", "-m", "playwright", "install", "chromium"])

        except Exception:
            print("Unable to install dependencies, check your python installation")

    if platform.system() == "Windows":
        try:
            run_command(["python", "-V"])
            run_command(["pip", "-V"])

        except Exception:
            print("Python is not installed, installing it via winget")

            try:
                run_command(["winget", "install", "python"])

            except Exception:
                print("Unable to install python, please install it manually")
                exit(1)

        run_command(["pip", "install", "toml"])
        run_command(["pip", "install", "playwright"])
        run_command(["python", "-m", "playwright", "install", "chromium"])


def run_command(command):
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_credentials():
    # Get intranet username and password
    print("\nIntroduce your intranet username and password:")
    username = input("Username: ")
    password = getpass("Password: ")

    # Check if the credentials are valid trying to login in the intranet
    print("Checking if the intranet username and password are valid")
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch()
        page = browser.new_page()

        try:
            # Navigate to login page
            page.goto(UPV_LOGIN_URL)

            # Fill login form and submit
            form = page.locator("form[name='alumno']")
            form.locator("input[name='dni']").fill(username)
            form.locator("input[name='clau']").fill(password)
            form.locator("input[type='submit']").click()

            # Check if login was successful
            assert page.title() == "Mi UPV"

        except AssertionError:
            print("The intranet username or password are not valid")
            # exit(1)

        except Exception as err:
            print(err)
            exit(1)


def install_script():
    install_dir = "/usr/local/reservation_bot"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    print(root_dir)
    if platform.system() == "Darwin":
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)

        print("Installing script...")
        shutil.copytree(root_dir, install_dir)


if __name__ == "__main__":
    main()
