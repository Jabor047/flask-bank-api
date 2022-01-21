## Bank API
This is an internal API for a fake financial institution using Python. it basic functionality is defined in the Tasks section below

### Usage
The whole application is dockerized you just run the docker container and you're good.
1. clone repo
2. run ``` docker-compose up --build ``` to build and start the containers.
3. To create a new account use the following ``` localhost:9090/create_account?customer_name=***&account_name=***&account_number=***&amount=**&account_type=*** ```, replacing the *** with values of course 😀
4. To retrieve balance use the following url format ``` localhost:9090/retrieve_balance?account_number=*** ```
5. To transfer an amount between different accounts ``` localhost:9090/transfer?source_account_number=***&target_account_number=***&amount=** ```
6. To get the transfer history for an account ``` localhost:9090/transferhistory?account_number=*** ```

### Testing
To run the unittests for the API, you run the following command ``` docker exec -it bank_api /usr/local/bin/python3 /app/tests/test_api.py ```

### Documentation
To view the documentation of the api go to the url ``` localhost:9090/ ```

## Challenge description
### Objective

Build an internal API for a fake financial institution using Python and any framework.

### Brief

While modern banks have evolved to serve a plethora of functions, at their core, banks must provide certain basic features. Today, your task is to build the basic HTTP API for one of those banks! Imagine you are designing a backend API for bank employees. It could ultimately be consumed by multiple frontends (web, iOS, Android etc).

### Tasks

- Implement assignment using:
  - Language: **Python**
  - Framework: **any framework**
- There should be API routes that allow them to:
  - Create a new bank account for a customer, with an initial deposit amount. A
    single customer may have multiple bank accounts.
  - Transfer amounts between any two accounts, including those owned by
    different customers.
  - Retrieve balances for a given account.
  - Retrieve transfer history for a given account.
- Write tests for your business logic

Feel free to pre-populate your customers with the following:

```json
[
  {
    "id": 1,
    "name": "Arisha Barron"
  },
  {
    "id": 2,
    "name": "Branden Gibson"
  },
  {
    "id": 3,
    "name": "Rhonda Church"
  },
  {
    "id": 4,
    "name": "Georgina Hazel"
  }
]
```

You are expected to design any other required models and routes for your API.