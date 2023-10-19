import sys

from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright, Page
from reservation import Reservation


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"
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
        reservation.reserve(page)


def login(page: Page, username: str, password: str):
    print("Iniciando sesión...")

    try:
        page.goto(UPV_LOGIN_URL)

        form = page.locator("form[name='alumno']")
        form.locator("input[name='dni']").fill(username)
        form.locator("input[name='clau']").fill(password)
        form.locator("input[type='submit']").click()

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
        # Intranet page
        page.locator("//div[@id='intranet']//a[2]").click()

        # Reservations page
        page.locator("//div[@id='subgrupo_1000']//table[@id='elemento_1001']").click()

    except Exception as err:
        print(f"Error al navegar a la pagina de reservas: {err}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
