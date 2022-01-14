import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.database import Base
from logger import setup_logger

logger = setup_logger("insert_data")
# for linux and windows systems uncomment below
docker_host_ip = "172.18.0.2"

# for mac os
# docker_host_ip = "host.docker.internal"
engine = create_engine(f"postgresql://docker:docker@{docker_host_ip}/docker")

Base.metadata.bind = engine

db = scoped_session(sessionmaker(bind=engine))

def create_customers():
    logger.info("Reading customers from customers.json")
    customers = open("/app/api/customers.json")
    customers = json.load(customers)

    for customer in customers:
        db.execute("INSERT INTO customers (name) VALUES (:n)", {"n": customer['name']})
        db.commit()
        logger.info("Successfully added customers into db")

if __name__ == "__main__":
    try:
        create_customers()
    except Exception as e:
        raise e
