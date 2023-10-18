from playwright.sync_api import sync_playwright

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
    Reservation("TENIS", "Martes 24/10/2023", "08:00-09:00", "TENIS 1"),
]


def run(playwright):
    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(5000)

    # Log in
    login(page, USERNAME, PASSWORD)

    # Navigate to the reservations page
    goto_revervations(page)

    print("Reservando pistas...")

    for reservation in RESERVATIONS:
        make_reservation(page, reservation)
        print(reservation)


def make_reservation(page, reservation: Reservation):
    # Select the sport
    page.locator(f"//select[@name='deporte']").select_option(reservation.sport)

    # Select the day
    page.get_by_role("button", name=reservation.date).click()

    # Select the court
    title = page.get_by_role("columnheader", name=reservation.court)

    # Select the time
    tabla = title.locator("xpath=ancestor::table[@class='upv_listacolumnas']")
    tabla.get_by_role("row", name=f"{reservation.time} Libre", exact=True).get_by_role(
        "link"
    ).click()

    # Confirm the reservation
    page.get_by_role("button", name="Cancel").click()


def goto_revervations(page):
    print("Navegando a reservas")

    # Enter intranet
    page.locator("//div[@id='intranet']//a[2]").click()

    # Enter reservation page
    page.locator("//div[@id='subgrupo_1000']//table[@id='elemento_1001']").click()


def login(page, username, password):
    print("Iniciando sesión...")

    # Go to the login page
    page.goto(UPV_LOGIN_URL)

    # Fill the login form and submit it
    form = page.locator("form[name='alumno']")
    form.locator("input[name='dni']").fill(username)
    form.locator("input[name='clau']").fill(password)
    form.locator("input[type='submit']").click()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
