import json
from dataclasses import dataclass

from bs4.element import Tag

from constansts import MONTH_NAMES
from utils.utils import identify_party


@dataclass
class LXIVDeputyHeaderInfo:
    """
    Extrae información de diputado de página principal.
    """

    header_table: Tag

    @staticmethod
    def clean_row_election_type(raw_election_type: str) -> dict:
        """
        Limpia y obtinen información de manera organizada
        del tipo de elección del diputado.
        """
        _, election_type = raw_election_type.split(":")

        return {"tipo_eleccion": election_type.strip()}

    @staticmethod
    def clean_row_alternate(raw_alternate: str) -> dict:
        """
        Limpia y obtinen información de manera organizada
        del suplente.
        """
        _, alternate = raw_alternate.split(":")

        return {"suplente": alternate.strip()}

    @staticmethod
    def clean_row_date_birth(raw_day_birth: str) -> dict:
        """
        Limpia y obtinen información de manera organizada
        la fecha de nacimiento.
        """
        _, date_birth = raw_day_birth.split(":")
        day, month_name, year = date_birth.upper().split("-")
        day = day.strip().zfill(2)
        month = MONTH_NAMES.get(month_name)
        final_date = f"{year}-{month}-{day}"

        return {"fecha_nacimiento": final_date}

    @staticmethod
    def clean_row_entity(raw_entity: str) -> dict:
        """
        Limpia y obtinen información de manera organizada
        de la entidad del diputado.
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

    @staticmethod
    def clean_row_email(raw_email: str) -> dict:
        """
        Limpia y obtinen información de manera organizada
        de email.
        """
        _, _, email, _, extension = raw_email.split()

        return {"email": email.strip(), "extension": extension.strip()}

    def get_party(self) -> dict:
        _, raw_party = self.header_table.find_all("img")
        raw_party = raw_party.attrs.get("src")
        party = identify_party(raw_party)

        return {"partido": party}

    def get_info(self):
        deputy_table = self.header_table.find("table")
        deputy_name, *rows = [row.text.strip() for row in deputy_table.find_all("tr")]

        election_type, entity, email, date_birth, alternate = rows

        deputy_info = {"diputado": deputy_name}
        deputy_info |= self.clean_row_election_type(election_type)
        deputy_info |= self.clean_row_entity(entity)
        deputy_info |= self.clean_row_email(email)
        deputy_info |= self.clean_row_date_birth(date_birth)
        deputy_info |= self.clean_row_alternate(alternate)
        deputy_info |= self.get_party()

        return deputy_info

    def __str__(self) -> None:
        return json.dumps(self.get_info(), indent=4)


if __name__ == "__main__":
    pass
