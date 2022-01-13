import unittest
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.models.database import Accounts, Base, Transactions
from api.logger import setup_logger
from api.app import db
from api import create_app

class BaseTestCase(unittest.TestCase):
    logger = setup_logger("unittest")
    URL = "http://127.0.0.1:5000"

    def test_index(self):
        response = requests.get(self.URL + '/')
        self.assertEqual(response.status_code, 200)

