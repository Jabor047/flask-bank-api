import os
import sys
from flask.json import jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask import request, Blueprint
from flasgger import swag_from

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.models.database import Accounts, Transactions
from api.logger import setup_logger
from api.models.database import create_tables
from api.insert_db import create_customers
from api.db_init import db, engine

logger = setup_logger("api")

bank = Blueprint("bank", __name__, url_prefix="/")

create_tables(engine, "docker")
create_customers("docker")

@bank.route("/create_account", methods=['POST'])
@swag_from("docs/create_account.yml")
def create_account():
    customer_name = request.args.get('customer_name', None)
    customer_name = customer_name.replace("%20", " ")
    account_name = request.args.get('account_name', None)
    account_number = request.args.get('account_number')
    amount = request.args.get('amount', None)
    account_type = request.args.get('account_type')

    if request.method == "POST":
        customer = db.execute("SELECT * FROM customers WHERE name = :c", {"c": customer_name}).fetchone()
        if customer is None:
            error = jsonify(success=False, status_code=400, message=f"{customer_name} doesn't exist")
            return error

        customer_id = customer["cust_id"]

        account = db.execute("SELECT * FROM accounts WHERE acc_number = :d", {"d": account_number}).fetchone()
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

        create_acc_error = jsonify(success=False, status_code=400, message=f"{account_number} already exists")
        return create_acc_error

@bank.route("/transfer", methods=["POST"])
@swag_from("docs/transfer.yml")
def transfer():
    source_acc_num = request.args.get('source_account_number')
    target_acc_num = request.args.get('target_account_number')
    amount = int(request.args.get('amount'))

    if request.method == "POST":
        if source_acc_num != target_acc_num:
            source_acc_bal = db.execute("SELECT * FROM accounts WHERE acc_number = :d",
                                        {"d": source_acc_num}).fetchone()

            target_acc_bal = db.execute("SELECT * FROM accounts WHERE acc_number = :d",
                                        {"d": target_acc_num}).fetchone()

            if source_acc_bal and target_acc_bal:
                if source_acc_bal["amount"] > amount:
                    try:
                        source_bal = source_acc_bal["amount"] - amount
                        target_bal = target_acc_bal["amount"] + amount

                        source_update = db.execute("UPDATE accounts set amount = :a WHERE acc_number = :b",
                                                   {"a": source_bal, "b": source_acc_num})
                        logger.info(f"updating source balance {source_acc_num}")
                        db.add(source_update)
                        db.commit()

                        source_trans = Transactions(acc_num=source_acc_num,
                                                    trans_msg=f"Transfered {amount} to {str(target_acc_num)}",
                                                    amount=amount,
                                                    transaction_type="withdraw")
                        logger.info(f"updating transactions for source account {source_acc_num}")
                        db.add(source_trans)
                        db.commit()

                        target_update = db.execute("UPDATE accounts set amount = :a WHERE acc_number = :b",
                                                   {"a": target_bal, "b": target_acc_num})
                        logger.info(f"updating source balance {target_acc_num}")
                        db.add(target_update)
                        db.commit()

                        target_trans = Transactions(acc_num=target_acc_num,
                                                    trans_msg=f"Transfered {amount} from {str(source_acc_num)}",
                                                    amount=amount,
                                                    transaction_type="deposit")
                        logger.info(f"updating transactions for source account {target_acc_num}")
                        db.add(target_trans)
                        db.commit()
                    except Exception as e:
                        raise e

                    transfer_success = jsonify(success=True, status_code=200,
                                               message=f"{amount} transfered from {source_acc_num} to {target_acc_num}")

                    return transfer_success
                else:
                    transfer_balance_error = jsonify(success=False, status_code=403,
                                                     message=f"{source_acc_num} has insufficient balance")
                    return transfer_balance_error
            elif source_acc_bal and target_acc_bal is None:
                transfer_account_error = jsonify(success=False, status_code=404,
                                                 message=f"Target account {target_acc_num} not Found")
                return transfer_account_error
            elif target_acc_bal and source_acc_bal is None:
                transfer_account_error = jsonify(success=False, status_code=404,
                                                 message=f"Source account {source_acc_num} not Found.")
                return transfer_account_error
            else:
                transfer_account_error = jsonify(success=False, status_code=404,
                                                 message="Both accounts not Found try different ones")
                return transfer_account_error
        else:
            same_transfer_account_error = jsonify(success=False, status_code=403,
                                                  message="Can't transfer to the same account")
            return same_transfer_account_error

@bank.route("/retrieve_balance", methods=["GET"])
@swag_from("docs/retrieve_balance.yml")
def retrieve_balance():
    account_number = request.args.get('account_number')

    if request.method == "GET":
        account = db.execute("SELECT * FROM accounts WHERE acc_number = :d", {"d": account_number}).fetchone()
        if account is None:
            balance_account_error = jsonify(success=False, status_code=404,
                                            message="Account not Found.try different one")
            return balance_account_error
        else:
            balance = db.execute("SELECT amount FROM Accounts WHERE acc_number = :d", {"d": account_number}).fetchone()
            if balance:
                balance_account = jsonify(success=False, status_code=200,
                                          message=f"Account balance is {balance['amount']}")
                return balance_account

@bank.route("/transferhistory", methods=["GET"])
@swag_from("docs/transfer_history.yml")
def retrieve_transfer_history():
    account_number = request.args.get("account_number")
    if request.method == "GET":

        account_transfer_his = db.execute("SELECT * FROM transactions WHERE acc_num = :a",
                                          {"a": account_number}).fetchone()

        if account_transfer_his is not None:
            transfer_history_success = jsonify(success=True, status_code=200, history=account_transfer_his)

            return transfer_history_success
        else:
            transfer_history_error = jsonify(success=False, status_code=404,
                                             message="Account not Found.try different one")
            return transfer_history_error


@bank.errorhandler(SQLAlchemyError)
def sql_error_handler(error):
    error = jsonify(success=False, status_code=400, error=str(error))
    return error
