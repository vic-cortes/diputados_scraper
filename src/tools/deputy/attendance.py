import re
from dataclasses import dataclass
from typing import Dict, List

import requests
from bs4 import BeautifulSoup, Tag

from constansts import Urls, MONTH_NAMES


NUMBER_PATTERN = r"([\s\d]+)"
MONTH_BORDER_COLOR = "#F2F2F2"
SESSION_DAY_BACKGROUND = "#D6E2E2"


def get_soup(url: str, params: dict = None) -> BeautifulSoup:
    if params is None:
        params = {}

    response = requests.get(url, params=params)
    return BeautifulSoup(response.content, "lxml")


@dataclass
class AttendanceCrawler:
    """
    Responsable de obtener el url del total de listados
    de periodo de sesiones.
    """

    deputy_id: int

    def get_session_metadata(self) -> List[Dict]:
        params = {"dipt": self.deputy_id}
        soup = get_soup(Urls.ATTENDANCE_URL, params=params)
        tables = soup.find_all("table")

        # La ultima tabla es la que cuenta con al informacion
        # de asistencias
        *_, last_table = tables

        # Buscar todos los renglones
        _, _, *sessions = last_table.find_all("tr")

        all_attendances_urls = []

        for session in sessions:

            if not (current_anchor := session.find("a")):
                continue

            endpoint = current_anchor.attrs.get("href")

            current_session = {
                "text": current_anchor.text.strip(),
                "href": f"{Urls.BASE_URL}/{endpoint}",
            }
            all_attendances_urls.append(current_session)

        return all_attendances_urls


@dataclass
class Attendance:
    """
    Obtiene las asistencias de la tabla de fechas de cada periodo de sesion.
    """

    session_attendance_url: str

    @staticmethod
    def _clean_calendar_table(calendar_table: Tag) -> List[Dict]:
        """
        Obtiene informacion del calendario de
        asistencias.
        """

        # El titulo de la tabla es la fecha
        date, *_ = calendar_table.find_all("tr")
        days = calendar_table.find_all("td")

        # Limpiar y estandarizar la fecha
        month, year = date.text.strip().upper().split()
        month_number = MONTH_NAMES.get(month)
        base_date = f"{year}-{month_number}"

        # Obtener los dias el cual hubo sesion. Cada dia con sesion
        # la celda esta marcada con verde #D6E2E2
        session_days = []

        for day in days:

            if day.attrs.get("bgcolor") != SESSION_DAY_BACKGROUND:
                continue

            day_number, *_ = re.findall(NUMBER_PATTERN, day.text)
            status = day.text.replace(day_number, "")
            day_number = day_number.zfill(2)

            status_day = {"date": f"{base_date}-{day_number}", "status": status}

            session_days.append(status_day)

        return session_days

    def get_attendance(self) -> List[Dict]:
        """
        Obtinene y filtra las tablas que cuenten con calendario
        """
        soup = get_soup(url=self.session_attendance_url)
        tables = soup.find_all("table")

        calendar_tables = []

        for table in tables:

            if table.attrs.get("bordercolorlight") != MONTH_BORDER_COLOR:
                continue

            clean_table = self._clean_calendar_table(table)
            calendar_tables.append(clean_table)

        flat_list = [item for sublist in calendar_tables for item in sublist]

        return flat_list


def run():
    deputy_attendance = AttendanceCrawler(deputy_id=2)


if __name__ == "__main__":
    run()
