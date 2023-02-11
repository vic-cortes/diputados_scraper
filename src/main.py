import requests
from bs4 import BeautifulSoup

from tools.deputy.attendance import AttendanceSessions, AttendanceCalendar
from tools.deputy.header_info import LXIVDeputyHeaderInfo


BASE_URL = "http://sitl.diputados.gob.mx/LXIV_leg"
CURRICULA_URL = f"{BASE_URL}/curricula.php"
ASISTENCIAS_URL = f"{BASE_URL}/asistencias_diputados_xperiodonplxiv.php"


response = requests.get(url=CURRICULA_URL, params={"dipt": 2})

html = response.content
# soup = BeautifulSoup(html, "lxml")

# tables = soup.find_all("table")
# _, information, *_ = tables

# html_table = information.find("table")

# # Encuentra la tabla de las comisiones que pertenece
# comision_table, *_ = [
#     table for table in tables if table.attrs.get("cellpadding") == "2"
# ]


if __name__ == "__main__":
    session = AttendanceSessions(deputy_id=2)
    list_sessions = session.get_list()

    all_attendance = []

    for session in list_sessions:
        session_url = session.get("href")
        current_attendance = AttendanceCalendar.get_data(session_url)

        all_attendance.append(current_attendance)

    flat_all_attendance_list = [item for sublist in all_attendance for item in sublist]

    flat_all_attendance_list
