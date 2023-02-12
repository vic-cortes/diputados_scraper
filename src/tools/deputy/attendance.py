import re
import json
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
class AttendanceSessions:
    """
    Responsable de obtener el url del total de listados
    de periodo de sesiones.
    """

    soup: Tag

    def get_list(self) -> List[Dict]:
        tables = self.soup.find_all("table")

        # La última tabla es la que cuenta con al información
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

    def __str__(self) -> None:
        return json.dumps(self.get_list(), indent=4)


@dataclass
class AttendanceCalendar:
    """
    Obtiene las asistencias de la tabla de fechas de cada período de sesión.
    """

    session_calendar_url: str

    @staticmethod
    def _clean_calendar_table(calendar_table: Tag) -> List[Dict]:
        """
        Obtiene información del calendario de
        asistencias.
        """
        # El título de la tabla es la fecha
        date, *_ = calendar_table.find_all("tr")
        days = calendar_table.find_all("td")

        # Limpiar y estandarizar la fecha
        month, year = date.text.strip().upper().split()
        month_number = MONTH_NAMES.get(month)
        base_date = f"{year}-{month_number}"

        # Obtener los días el cual hubo sesión. Cada día con sesión
        # la celda está marcada con verde #D6E2E2
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
        soup = get_soup(url=self.session_calendar_url)
        tables = soup.find_all("table")

        calendar_tables = []

        for table in tables:

            if table.attrs.get("bordercolorlight") != MONTH_BORDER_COLOR:
                continue

            clean_table = self._clean_calendar_table(table)
            calendar_tables.append(clean_table)

        flat_calendar_list = [item for sublist in calendar_tables for item in sublist]

        return flat_calendar_list

    @classmethod
    def get_data(cls, url: str) -> List[Dict]:
        calendar = cls(session_calendar_url=url)
        return calendar.get_attendance()


def run():
    session = AttendanceSessions(deputy_id=2)
    list_sessions = session.get_list()

    all_attendance = []

    for session in list_sessions:
        session_url = session.get("href")
        current_attendance = AttendanceCalendar.get_data(session_url)

        all_attendance.append(current_attendance)

    flat_all_attendance_list = [item for sublist in all_attendance for item in sublist]

    return flat_all_attendance_list


if __name__ == "__main__":
    run()
