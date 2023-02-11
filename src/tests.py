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

    def test_path_name(self) -> None:
        print_title("Test find tables")

        tables = self.soup.find_all("table")

        self.assertEqual(len(tables), 17)


if __name__ == "__main__":
    unittest.main()
