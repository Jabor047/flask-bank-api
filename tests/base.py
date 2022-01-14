import imp
import unittest
import requests
import sys
import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import query, scoped_session, sessionmaker
from flask import request
from api.insert_db import create_customers

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.models.database import Base, create_tables
from api.logger import setup_logger
from api.app import db

ip_address = socket.gethostbyname(socket.gethostname())

class BaseTestCase(unittest.TestCase):
    logger = setup_logger("unittest")
    URL = f"http://{ip_address}:5000"

    db.execute("DELETE FROM transactions")
    db.commit()

    db.execute("DELETE FROM accounts")
    db.commit()

    db.execute("DELETE FROM customers")
    db.commit()

    create_customers("docker")

    def test_index(self):
        self.logger.info("Tesing Index URL")
        response = requests.get(self.URL + '/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.mai()
