import unittest
import requests
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.models.database import Base
from api.logger import setup_logger


class BaseTestCase(unittest.TestCase):
    logger = setup_logger("unittest")
    URL = "http://127.0.0.1:5000"

    docker_host_ip = "172.17.0.2"

    # for mac os
    # docker_host_ip = "host.docker.internal"
    engine = create_engine(f"postgresql://docker:docker@{docker_host_ip}/docker")

    Base.metadata.bind = engine

    db = scoped_session(sessionmaker(bind=engine))

    def test_index(self):
        self.logger.info("Tesing Index URL")
        response = requests.get(self.URL + '/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.mai()
