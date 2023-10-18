import datetime


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
