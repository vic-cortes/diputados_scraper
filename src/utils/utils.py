from constansts import PARTIES


def identify_party(raw_party: str) -> str:
    """
    Identifica el nombre del partido
    a traves del nombre del archivo del logo
    """
    raw_party = raw_party.lower()

    for party_alias, party_name in PARTIES.items():

        if party_alias in raw_party:
            return party_name

    return f"NO_IDENTIFICADO/{raw_party}"


def print_title(title: str) -> None:
    DEL = "*" * 10
    print(f"{DEL} {title.upper()} {DEL}")
