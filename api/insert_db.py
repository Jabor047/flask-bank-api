import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.database import Base
from logger import setup_logger
from api.db_init import db

logger = setup_logger("insert_data")

def create_customers(db_name):

    logger.info("Reading customers from customers.json")
    customers = open("/app/api/customers.json")
    customers = json.load(customers)

    for customer in customers:
        db.execute("INSERT INTO customers (name) VALUES (:n)", {"n": customer['name']})
        db.commit()
        logger.info("Successfully added customers into db")
