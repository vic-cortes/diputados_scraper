import requests
from bs4 import BeautifulSoup

from tools.deputy.header_info import DeputyHeaderInfo


BASE_URL = "http://sitl.diputados.gob.mx/LXIV_leg/curricula.php"


response = requests.get(url=BASE_URL, params={"dipt": 2})

html = response.content
soup = BeautifulSoup(html, "lxml")

tables = soup.find_all("table")
_, information, *_ = tables

html_table = information.find("table")


if __name__ == "__main__":
    deputy = DeputyHeaderInfo(header_table=html_table)

    print(deputy)
