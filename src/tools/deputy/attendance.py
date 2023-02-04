from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from constansts import Urls


@dataclass
class AttendanceCrawler:
    deputy_id: int

    @staticmethod
    def _get_soup(url: str, params: dict) -> BeautifulSoup:
        response = requests.get(url, params=params)
        return BeautifulSoup(response.content, "lxml")

    def get_attendance_years_url(self) -> None:
        params = {"dipt": self.deputy_id}
        soup = self._get_soup(Urls.ATTENDANCE_URL, params=params)
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


class Attendance:
    pass


def run():
    deputy_attendance = AttendanceCrawler(deputy_id=2)

    soup = deputy_attendance.get_attendance_years_url()


if __name__ == "__main__":
    run()
