from api.models.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from api.logger import setup_logger
import json

logger = setup_logger("insert_data")
docker_host_ip = "172.17.0.1"
engine = create_engine(f"postgres://docker:docker@{docker_host_ip}/docker")

Base.metadata.bind = engine

db = scoped_session(sessionmaker(bind=engine))

def create_customers():
    logger.info("Reading customers from customers.json")
    customers = open("customers.json")
    customers = json.load(customers)

    for customer in customers:
        db.execute("INSERT INTO Customers (name) VALUES (:n)", {"n": customer['name']})
        db.commit()
        logger.info("Successfully added customers into db")

if __name__ == "__main__":
    try:
        create_customers()
    except Exception as e:
        raise e
