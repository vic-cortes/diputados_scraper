import requests
from bs4 import BeautifulSoup

from tools.deputy.attendance import AttendanceCrawler
from tools.deputy.header_info import DeputyHeaderInfo


BASE_URL = "http://sitl.diputados.gob.mx/LXIV_leg"
CURRICULA_URL = f"{BASE_URL}/curricula.php"
ASISTENCIAS_URL = f"{BASE_URL}/asistencias_diputados_xperiodonplxiv.php"


# response = requests.get(url=CURRICULA_URL, params={"dipt": 2})

# html = response.content
# soup = BeautifulSoup(html, "lxml")

# tables = soup.find_all("table")
# _, information, *_ = tables

# html_table = information.find("table")

# # Encuentra la tabla de las comisiones que pertenece
# comision_table, *_ = [
#     table for table in tables if table.attrs.get("cellpadding") == "2"
# ]


if __name__ == "__main__":
    deputy_attendance = AttendanceCrawler(deputy_id=2)

    list_attendance = deputy_attendance.get_attendance_years_url()

    print(list_attendance)
