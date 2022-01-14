import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

logger = setup_logger("database")
Base = declarative_base()

class Customers(Base):

    __tablename__ = "customers"
    cust_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    acc = relationship("Accounts")

    def __init__(self, name) -> None:
        self.name = name

class Accounts(Base):

    __tablename__ = "accounts"
    acc_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_name = Column(String(50), nullable=False)
    acc_number = Column(Integer, unique=True)
    acc_type = Column(String(20), nullable=False)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.cust_id"), nullable=False)
    last_update = Column(DateTime(timezone=False), default=datetime.datetime.now())
    trans_id = relationship("Transactions")

    def __init__(self, name, number, amount, customer_id, acc_type="Current") -> None:
        self.acc_name = name
        self.acc_number = number
        self.acc_type = acc_type
        self.amount = amount
        self.customer_id = customer_id

class Transactions(Base):

    __tablename__ = "transactions"
    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_num = Column(Integer, ForeignKey("accounts.acc_number"), nullable=False)
    trans_msg = Column(String(250), nullable=False)
    amount = Column(Integer, nullable=False)
    trans_type = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.now())

    def __init__(self, acc_num, trans_msg, amount, transaction_type="transfer") -> None:
        self.acc_num = acc_num
        self.trans_msg = trans_msg
        self.amount = amount
        self.transaction_type = transaction_type

def create_tables():
    try:
        # for linux and windows systems uncomment below
        docker_host_ip = "172.18.0.2"

        # for mac os
        # docker_host_ip = "host.docker.internal"
        engine = create_engine(f"postgresql://docker:docker@{docker_host_ip}/docker", echo=True)
        Base.metadata.create_all(engine)
        logger.info("All Models Created Successfully")
    except Exception as e:
        raise e

if __name__ == "__main__":
    create_tables()
