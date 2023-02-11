import os
import unittest

from bs4 import BeautifulSoup

from tools.deputy.header_info import LXIVDeputyHeaderInfo
from utils.utils import print_title

DATA_PATH = os.path.join(os.path.dirname(__file__), "test_data")


class DeputyHeaderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.html = open(f"{DATA_PATH}/test_deputy_main_page.html", "r").read()
        self.soup = BeautifulSoup(self.html, "lxml")
        self.header_table = self.soup.find_all("table")[
            1
        ]  # Header table es el segundo elemento
        self.header_table = self.header_table.find("table")

    @unittest.skip("")
    def test_path_name(self) -> None:
        print_title("Test find tables")
        tables = self.soup.find_all("table")
        self.assertEqual(len(tables), 17)

    # @unittest.skip("")
    def test_header_deputy(self) -> None:
        print_title("test header")
        deputy_header = LXIVDeputyHeaderInfo(header_table=self.header_table)
        print(deputy_header)
        self.assertIsInstance(deputy_header.get_info(), dict)


if __name__ == "__main__":
    unittest.main()
