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

ip_address = socket.gethostbyname(socket.gethostname())
create_tables('test')
create_customers("test")

class BaseTestCase(unittest.TestCase):
    logger = setup_logger("unittest")
    URL = f"http://{ip_address}:5000"

    docker_host_ip = "172.18.0.2"

    # for mac os
    # docker_host_ip = "host.docker.internal"
    engine = create_engine(f"postgresql://docker:docker@{docker_host_ip}/test")

    Base.metadata.bind = engine

    db = scoped_session(sessionmaker(bind=engine))

    truncate_customers = db.execute("TRUNCATE TABLE customers")
    db.add(truncate_customers)
    db.commit()

    truncate_accounts = db.execute("TRUNCATE TABLE accounts")
    db.add(truncate_accounts)
    db.commit()

    def test_index(self):
        self.logger.info("Tesing Index URL")
        response = requests.get(self.URL + '/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.mai()
