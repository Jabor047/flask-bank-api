import unittest
import requests
import sys
import os

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
        self.assertEqual(response.status_code, 200)
        self.assertIn("account Successfully added", response.message)

    def test_create_account_customer_name_fail(self):
        params = {
            "customer_name": "Kevin%20KArobia",
            "account_name": "test",
            "account_number": "8889",
            "amount": "56",
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        self.assertEqual(response.status_code, 400)
        self.assertIn("doesn't exist", response.message)

    def test_create_account_account_exists(self):
        params = {
            "customer_name": "Georgina%20Hazel",
            "account_name": "test",
            "account_number": "0009",
            "amount": "300",
            "account_type": "test"
        }

        response = requests.post(self.URL + '/create_account', params=params)
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.message)

    def delete_test_accounts(self):
        account_number = "0009"
        query = self.db.Execute("DELETE FROM accounts WHERE account_number = :d",
                                {"d": account_number})
        self.db.add(query)
        self.db.commit()
        self.logger.info("Successfully deleted the test account")


if __name__ == "__main__":
    unittest.main()