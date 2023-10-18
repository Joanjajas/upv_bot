from getpass import getpass
import datetime
import sys

from playwright.sync_api import sync_playwright

UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"


def run(playwright):
    # sport = input("Deporte: ").upper()
    # date = get_day_of_week_spanish(input("Fecha (dd/mm/yyyy): "))
    sport = "PADEL"
    date = get_day_of_week_spanish("20/10/2023")

    print(date)

    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(5000)

    # Log in
    login(page, USERNAME, PASSWORD)

    # Log in and navigate to the grades page
    goto_revervations(page)

    # Make the reservation
    make_reservation(page, sport, date)

    input("")


def make_reservation(page, sport, date):
    try:
        # Select the sport
        page.locator(f"//select[@name='deporte']").select_option(sport)

        # Select the day
        print(date)
        page.get_by_text(date).click()

    except Exception as err:
        print(f"Error ocurred while selecting sport: {err}", file=sys.stderr)
        exit(1)


# Function to get the name of the day of the week in Spanish
def get_day_of_week_spanish(date):
    days_of_week = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
    day_of_week = days_of_week[date_obj.weekday()]

    return f"{day_of_week} {date}"


def goto_revervations(page):
    try:
        print("Navigating to reservations page...")

        # Enter intranet
        page.locator("//div[@id='intranet']//a[2]").click()

        # Enter reservation page
        algo = page.locator(
            "//div[@id='subgrupo_1000']//table[@id='elemento_1001']"
        ).click()
        print(algo)

    except Exception as err:
        print(f"Error ocurred while navigating to reservations: {err}", file=sys.stderr)
        exit(1)


def login(page, username, password):
    print("Logging in...")

    try:
        # Go to the login page
        page.goto(UPV_LOGIN_URL)

        # Fill the login form and submit it
        form = page.locator("form[name='alumno']")
        form.locator("input[name='dni']").fill(username)
        form.locator("input[name='clau']").fill(password)
        form.locator("input[type='submit']").click()

        # Check if the login was succesfull
        assert page.title() == "Mi UPV"

    except AssertionError:
        print(
            "Login failed. Make sure to use a valid username and password.",
            file=sys.stderr,
        )
        exit(1)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
