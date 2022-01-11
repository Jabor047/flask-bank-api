import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from logger import setup_logger

logger = setup_logger("database")
Base = declarative_base()

class Customers(Base):

    __tablename__ = "Customers"
    cust_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    acc_id = relationship("Accounts")

    def __init__(self, name) -> None:
        self.name = name

class Accounts(Base):

    __tablename__ = "Accounts"
    acc_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_name = Column(String(50), nullable=False)
    acc_number = Column(Integer, unique=True)
    acc_type = Column(String(20), nullable=False)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey("Customers.cust_id"))
    last_update = Column(DateTime(timezone=False), default=datetime.datetime.now())
    trans_id = relationship("Transactions")

    def __init__(self, name, number, amount, customer_id, acc_type="Current") -> None:
        self.acc_name = name
        self.acc_number = number
        self.acc_type = acc_type
        self.amount = amount
        self.customer_id = customer_id

class Transactions(Base):

    __tablename__ = "Transactions"
    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_num = Column(Integer, ForeignKey("Accounts.acc_number"), nullable=False)
    trans_msg = Column(String(250), nullable=False)
    amount = Column(Integer, nullable=False)
    trans_type = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.now())

    def __init__(self, acc_num, trans_msg, amount, transaction_type="transfer") -> None:
        self.acc_num = acc_num
        self.trans_msg = trans_msg
        self.amount = amount
        self.transaction_type = transaction_type

if __name__ == "__main__":
    try:
        docker_host_ip = "172.17.0.1"
        engine = create_engine(f"postgres://docker:docker@{docker_host_ip}/docker")
        Base.metadata.create_all(engine)
        logger.info("All Models Created Successfully")
    except Exception as e:
        raise e
