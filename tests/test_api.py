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
            "account_number": 9,
            "amount": 300,
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        response = response.content.decode("utf-8")
        response = json.loads(response)
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
        response = response.content.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 400)
        self.assertIn("doesn't exist", response["message"])

    def test_create_account_zaccount_exists(self):
        params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": 9,
            "amount": 300,
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        response = response.content.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 400)
        self.assertIn("already exists", response["message"])

    def test_transfer_csuccess(self):
        account_params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": 10,
            "amount": 300,
            "account_type": "test"
        }

        post_response = requests.post(self.URL + '/create_account', params=account_params)
        post_response = post_response.content
        post_response = post_response.decode("utf-8")

        transfer_params = {
            "source_account_number": 9,
            "target_account_number": 10,
            "amount": 100
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(200, response["status_code"])
        self.assertIn("transfered from", response["message"])

    def test_transfer_insufficient_balance(self):
        transfer_params = {
            "source_account_number": 9,
            "target_account_number": 10,
            "amount": 400
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        # pp(response)
        self.assertEqual(response["status_code"], 403)
        self.assertIn("insufficient balance", response["message"])

    def test_transfer_target_account_exists_not(self):
        transfer_params = {
            "source_account_number": 9,
            "target_account_number": 11,
            "amount": 400
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Target account", response["message"])

    def test_transfer_zsource_account_exists_not(self):
        transfer_params = {
            "source_account_number": 8,
            "target_account_number": 10,
            "amount": 400
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        # pp(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Source account", response["message"])

    def test_transfer_both_accounts_exist_not(self):
        transfer_params = {
            "source_account_number": 8,
            "target_account_number": 11,
            "amount": 400
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Both accounts not Found", response["message"])

    def test_transfer_same_account_transfer(self):
        transfer_params = {
            "source_account_number": 9,
            "target_account_number": 9,
            "amount": 400
        }

        response = requests.post(self.URL + "/transfer", params=transfer_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 403)
        self.assertIn("Can't transfer to the same account", response["message"])

    def test_retrive_balance_success(self):
        retrieve_balance_params = {
            "account_number": 9
        }
        response = requests.get(self.URL + "/retrieve_balance", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 200)
        self.assertIn("Account balance is", response["message"])

    def test_retrive_balance_account_exists_not(self):
        retrieve_balance_params = {
            "account_number": 8
        }
        response = requests.get(self.URL + "/retrieve_balance", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Account not Found", response["message"])

    def test_transferhistory_success(self):
        retrieve_balance_params = {
            "account_number": 9
        }
        response = requests.get(self.URL + "/transferhistory", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 200)

    def test_transferhistory_fail(self):
        retrieve_balance_params = {
            "account_number": 8
        }
        response = requests.get(self.URL + "/transferhistory", params=retrieve_balance_params)
        response = response.content
        response = response.decode("utf-8")
        response = json.loads(response)
        self.assertEqual(response["status_code"], 404)
        self.assertIn("Account not Found", response["message"])


if __name__ == "__main__":
    unittest.main()
