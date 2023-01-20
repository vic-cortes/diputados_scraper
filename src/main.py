import requests
from bs4 import BeautifulSoup


MONTH_NAMES = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12",
}
BASE_URL = "http://sitl.diputados.gob.mx/LXIV_leg/curricula.php"


response = requests.get(url=BASE_URL, params={"dipt": 1})

html = response.content
soup = BeautifulSoup(html, "lxml")

tables = soup.find_all("table")
_, information, *_ = tables

html_table = information.find("table")
candidate_table = html_table.find("table")
candidate_name, *rows = [row.text.strip() for row in candidate_table.find_all("tr")]

election_type, entity, email, date_birth, alternate = rows


class DeputyHeaderInfo:
    def clean_row_election_type(raw_election_type: str) -> dict:
        """
        Limpia y obtinen la informacion de manera organizada
        del tipo de eleccion del diputado
        """
        _, election_type = raw_election_type.split(":")

        return {"tipo_eleccion": election_type.strip()}

    def clean_row_alternate(raw_alternate: str) -> dict:
        """
        Limpia y obtinen la informacion de manera organizada
        del tipo de eleccion del diputado
        """
        _, alternate = raw_alternate.split(":")

        return {"suplente": alternate.strip()}

    def clean_row_birth_day(raw_day_birth: str) -> dict:
        """
        Limpia y obtinen la informacion de manera organizada
        la fecha de nacimiento
        """
        _, date_birth = raw_day_birth.split(":")
        day, month_name, year = date_birth.upper().split("-")
        day = day.strip().zfill(2)
        month = MONTH_NAMES.get(month_name)
        final_date = f"{year}-{month}-{day}"

        return {"fecha_nacimiento": final_date}

    def clean_row_entity(raw_entity: str) -> dict:
        """
        Limpia y obtinen la informacion de manera organizada
        de la entdidad del diputado
        """
        entity_name, district, district_code = [
            el.strip() for el in raw_entity.split("|")
        ]

        _, state = entity_name.split(":")
        _, district = district.split(":")

        return {
            "entidad": state.strip(),
            "distrito": district.strip(),
            "codig_distrito": district_code.strip(),
        }

    def clean_row_email(raw_email: str) -> dict:
        """
        Limpia y obtinen la informacion de manera organizada
        del renglon de email
        """
        _, _, email, _, extension = raw_email.split()

        return {"email": email.strip(), "extension": extension.strip()}
