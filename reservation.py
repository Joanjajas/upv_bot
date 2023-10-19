import toml

from playwright.sync_api import Page
from logger import log


class Reservation:
    def __init__(self, sport, date, time, court):
        self.sport = sport
        self.date = date
        self.time = time
        self.court = court

    def reserve(self, page: Page):
        try:
            # Select the sport
            page.locator(f"//select[@name='deporte']").select_option(self.sport)

            # Select the day
            page.get_by_role("button", name=self.date).click()

            # Select the table corresponding to the court
            court = page.get_by_role("columnheader", name=self.court)

            # Select the time
            court_table = court.locator(
                "xpath=ancestor::table[@class='upv_listacolumnas']"
            )
            court_table.get_by_role(
                "row", name=f"{self.time} Libre", exact=True
            ).get_by_role("link").click()

            page.get_by_role("button", name="Cancel").click()
            log(str(self))

        except Exception:
            log(
                f"Error al reservar la pista de {self.sport}: La pista ya está reservada",
                level="WARNING",
            )

    def __str__(self):
        return f"Reservada pista de {self.sport} el {self.date} de {self.time} en la pista {self.court}"


def load_from_toml_file(file_path: str):
    try:
        data = toml.load(file_path)
        reservations = data.get("reserva", [])

        return [
            Reservation(
                reservation["deporte"],
                reservation["fecha"],
                reservation["hora"],
                reservation["pista"],
            )
            for reservation in reservations
        ]

    except Exception as e:
        log(f"Error leyendo las reservas: {e}", level="ERROR")
        exit(1)
