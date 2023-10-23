import subprocess
from getpass import getpass

from playwright.sync_api import sync_playwright

UPV_LOGIN_URL = "https://intranet.upv.es"


def main():
    install_deps()
    get_credentials()


def install_deps():
    print("Installing dependencies...")
    subprocess.run(["/usr/bin/python3", "-m", "pip", "install", "playwright"])
    subprocess.run(["/usr/bin/python3", "-m", "playwright", "install", "chromium"])
    subprocess.run(["/usr/bin/python3", "-m", "pip", "install", "toml"])


def get_credentials():
    # Get intranet username and password
    print("Introduce your intranet username and password:")
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
            exit(1)

        except Exception as err:
            print(err)
            exit(1)


if __name__ == "__main__":
    main()
