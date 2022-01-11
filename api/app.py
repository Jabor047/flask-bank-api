from flask.json import jsonify
from api.models.database import Accounts, Base
from api.logger import setup_logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, request, redirect, url_for


app = Flask(__name__)
logger = setup_logger("api")
docker_host_ip = "172.17.0.1"
engine = create_engine(f"postgres://docker:docker@{docker_host_ip}/docker")

Base.metadata.bind = engine

db = scoped_session(sessionmaker(bind=engine))

@app.route("/create_account", methods=['POST', 'GET'])
def create_account():
    customer_name = request.args.get('customer_name', None)
    account_name = request.args.get('account_name', None)
    account_number = request.args.get('account_number')
    amount = request.args.get('amount', None)
    account_type = request.args.get('account_type')

    if request.method == "POST":
        customer = db.execute("SELECT * FROM Customers WHERE name = :c", {"c": customer_name}).fetchone()
        if customer is None:
            error = jsonify(success=False, status_code=400, message=f"{customer_name} doesn't exist")
            return error

        customer_id = customer["cust_id"]

        account = db.execute("SELECT * FROM Accounts WHERE account_number = :d", {"d": account_number}).fetchone()
        if account is None:
            try:
                query = Accounts(name=account_name, number=account_number, amount=amount, customer_id=customer_id,
                                 acc_type=account_type)

                db.add(query)
                db.commit()
            except Exception as e:
                raise e

            success = jsonify(success=True, status_code=200, message=f"{account_name} account Successfully added")

            return success

        error = jsonify(success=False, status_code=400, message=f"{account_name} already exists")
        return error

@app.errorhandler(SQLAlchemyError)
def sql_error_handler(error):
    error = jsonify(success=False, status_code=400, error=str(error))
    return error
