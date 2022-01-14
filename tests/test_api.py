import unittest
import requests
import sys
import os
import json
from pprint import pprint as pp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseTestCase

class BankApiTestCase(BaseTestCase):
    def test_create_account_success(self):
        params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": "0009",
            "amount": "300",
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 200)
        self.assertIn("account Successfully added", response["message"])

    def test_create_account_customer_name_fail(self):
        params = {
            "customer_name": "Kevin%20KArobia",
            "account_name": "test",
            "account_number": "8889",
            "amount": "56",
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 400)
        self.assertIn("doesn't exist", response["message"])

    def test_create_account_account_exists(self):
        params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": "0009",
            "amount": "300",
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 400)
        self.assertIn("already exists", response["message"])

    def test_transfer_success(self):
        account_params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": "0010",
            "amount": "300",
            "account_type": "test"
        }

        requests.post(self.URL + '/create_account', params=account_params)

        transfer_params = {
            "source_acc_num": "0009",
            "target_acc_num": "0010",
            "amount": "100"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(200, response["status_code"])
        self.assertIn("transfered from", response["message"])

    def test_transfer_insufficient_balance(self):
        transfer_params = {
            "source_acc_num": "0009",
            "target_acc_num": "0010",
            "amount": "400"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 403)
        self.assertIn("insufficient balance", response["message"])

    def test_transfer_target_account_exists_not(self):
        transfer_params = {
            "source_acc_num": "0009",
            "target_acc_num": "0011",
            "amount": "400"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Target account", response["message"])

    def test_transfer_source_account_exists_not(self):
        transfer_params = {
            "source_acc_num": "0008",
            "target_acc_num": "0010",
            "amount": "400"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Source account", response["message"])

    def test_transfer_both_accounts_exist_not(self):
        transfer_params = {
            "source_acc_num": "0008",
            "target_acc_num": "0011",
            "amount": "400"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Both accounts not Found", response["message"])

    def test_transfer_same_account_transfer(self):
        transfer_params = {
            "source_acc_num": "0009",
            "target_acc_num": "0009",
            "amount": "400"
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 403)
        self.assertIn("Can't transfer to the same account", response["message"])

    def test_retrive_balance_success(self):
        retrieve_balance_params = {
            "account_number": "0009"
        }
        response = requests.get(self.URL + "/retrieve_balance", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 200)
        self.assertIn("Account balance is", response["message"])

    def test_retrive_balance_account_exists_not(self):
        retrieve_balance_params = {
            "account_number": "0008"
        }
        response = requests.get(self.URL + "/retrieve_balance", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Account not Found", response["message"])

    def test_transferhistory_success(self):
        retrieve_balance_params = {
            "account_number": "0009"
        }
        response = requests.get(self.URL + "/transferhistory", params=retrieve_balance_params)
        response = response.content
        pp(response)
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 200)

    def test_transferhistory_fail(self):
        retrieve_balance_params = {
            "account_number": "0009"
        }
        response = requests.get(self.URL + "/transferhistory", params=retrieve_balance_params)
        response = response.content
        pp(response)
        response = response.decode("utf-8")
        response = json.loads(response)
        pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Account not Found", response["message"])
        self.delete_test_accounts()

    def delete_test_accounts(self):
        account_number = "0009"
        query = self.db.Execute("DELETE FROM accounts WHERE account_number = :d",
                                {"d": account_number})
        self.db.add(query)
        self.db.commit()

        account_number_two = "0010"
        query_two = self.db.Execute("DELETE FROM accounts WHERE account_number = :d",
                                    {"d": account_number_two})
        self.db.add(query_two)
        self.db.commit()
        self.logger.info("Successfully deleted the test accounts")


if __name__ == "__main__":
    unittest.main()
