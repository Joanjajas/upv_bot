import sys

from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright, Page


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"


class Reservation:
    def __init__(self, sport, date, time, court):
        self.sport = sport
        self.date = date
        self.time = time
        self.court = court

    def __str__(self):
        return f"Reservada pista de {self.sport} el {self.date} de {self.time} en la pista {self.court}"


RESERVATIONS = [
    Reservation("PADEL", "Sábado 21/10/2023", "08:00-09:00", "PÁDEL EXTERIOR 2"),
    Reservation("TENIS", "Martes 24/10/2023", "08:00-09:00", "TENIS 2"),
]


def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.set_default_timeout(5000)

    login(page, USERNAME, PASSWORD)
    navigate_to_reservations(page)

    print("Reservando pistas...")

    for reservation in RESERVATIONS:
        make_reservation(page, reservation)


def login(page: Page, username: str, password: str):
    print("Iniciando sesión...")

    try:
        # Go to the login page
        page.goto(UPV_LOGIN_URL)

        # Fill the login form and submit it
        form = page.locator("form[name='alumno']")
        form.locator("input[name='dni']").fill(username)
        form.locator("input[name='clu']").fill(password)
        form.locator("input[type='submit']").click()

        # Check if the login was succesfull
        assert page.title() == "Mi UPV"

    except AssertionError:
        print(
            "Error al iniciar sesión. Asegurate de introducir un usuario y contraseña válidos",
            file=sys.stderr,
        )
        exit(1)

    except Exception as err:
        print(f"Error al iniciar sesión: {err}", file=sys.stderr)
        exit(1)


def navigate_to_reservations(page: Page):
    print("Navegando a reservas")

    try:
        # Enter intranet
        page.locator("//div[@id='intranet']//a[2]").click()

        # Enter reservation page
        page.locator("//div[@id='subgrupo_1000']//table[@id='elemento_1001']").click()

    except Exception as err:
        print(f"Error al navegar a la pagina de reservas: {err}", file=sys.stderr)
        exit(1)


def make_reservation(page: Page, reservation: Reservation):
    try:
        # Select the sport
        page.locator(f"//select[@name='deporte']").select_option(reservation.sport)

        # Select the day
        page.get_by_role("button", name=reservation.date).click()

        # Select the table corresponding to the court
        court = page.get_by_role("columnheader", name=reservation.court)

        # Select the time
        court_table = court.locator("xpath=ancestor::table[@class='upv_listacolumnas']")
        court_table.get_by_role(
            "row", name=f"{reservation.time} Libre", exact=True
        ).get_by_role("link").click()

        page.get_by_role("button", name="Cancel").click()
        print(reservation)

    except Exception as err:
        print(
            f"Error al reservar la pista de {reservation.sport}: {err}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
