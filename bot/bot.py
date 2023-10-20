from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright, Page
from reservation import load_from_toml_file
from logger import log


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"


def run(playwright: Playwright):
    # Get reservations from TOML file
    reservations = load_from_toml_file("~/bot_reservas/reservas.toml")

    # Launch new instance of Chromium and create a new page
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    # Set default timeout to 5 seconds
    page.set_default_timeout(5000)

    # Login and navigate to reservations page
    login(page, USERNAME, PASSWORD)
    navigate_to_reservations(page)

    log("Reservando pistas...")

    # Make all reservations
    for reservation in reservations:
        reservation.reserve(page)


def login(page: Page, username: str, password: str):
    log("Iniciando sesión...")

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
        log(
            "Error al iniciar sesión. Asegurate de introducir un usuario y contraseña válidos",
            level="ERROR",
        )
        exit(1)

    except Exception as err:
        log(f"Error al iniciar sesión: {err}", level="ERROR")
        exit(1)


def navigate_to_reservations(page: Page):
    log("Navegando a la página de reservas...")

    try:
        # Intranet page
        page.locator("//div[@id='intranet']//a[2]").click()

        # Reservations page
        page.locator("//div[@id='subgrupo_1000']//table[@id='elemento_1001']").click()

    except Exception as err:
        log(f"Error al navegar a la pagina de reservas: {err}", level="ERROR")
        exit(1)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
