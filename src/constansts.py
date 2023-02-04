from enum import Enum


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


class Parties(Enum):
    PAN = "pan"
    PRI = "pri"
    PT = "pt"
    MORENA = "morena"
    PRD = "prd"


PARTIES = {party.value: party.name for party in list(Parties)}


class Urls:
    BASE_URL = "http://sitl.diputados.gob.mx/LXIV_leg"
    CURRICULA_URL = f"{BASE_URL}/curricula.php"
    ATTENDANCE_URL = f"{BASE_URL}/asistencias_diputados_xperiodonplxiv.php"
