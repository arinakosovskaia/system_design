Here's the interaction between the services

![](/Users/arina/Documents/GitHub/system_design/task3/pic.png "PIC")

**Authorization Service**

The Authorization Service is responsible for handling user registration and login, ensuring secure authentication and the issuance of access tokens.

**Endpoints:**

User Registration

    Endpoint: POST /users/register
    Description: Allows users to register by providing essential details such as email, password, and contact information.
    Responses:
    200: User successfully registered.
    400: Bad request if some data is missing or if the email or username already exists.

User Login

    Endpoint: POST /users/token
    Description: Authenticates users based on their login credentials and issues a secure access token.
    Responses:
    200: Access token successfully created.
    401: Incorrect username or password if the login credentials are incorrect.

**Billing Service**

The Billing Service manages user accounts, facilitating deposit, withdrawal, and balance check operations.

**Endpoints:**

Deposit Money

    Endpoint: POST /billing/deposit
    Description: Enables users to deposit money into their accounts, updating their account balance.
    Responses:
    200: Money deposited successfully.
    400: Bad request if the request is malformed.
    404: User not found if the user associated with the token is not found.

Check balance

    Endpoint: GET /billing/balance
    Description: Retrieves and displays the current account balance of the authenticated user.
    Responses:
    200: Balance checked with the user's current balance.
    404: User not found if the user associated with the token is not found.
    Withdraw Money:

Withdraw Money

    Endpoint: POST /billing/withdraw
    Description: Facilitates the withdrawal of funds from the user's account, updating the account balance accordingly.
    Responses:
    200: Money withdrawn successfully.
    400: Bad request if the request is malformed.
    404: User not found if the user associated with the token is not found.

**Order Service**

The Order Service manages the creation and retrieval of user orders.

**Endpoints:**

Create Order

    Endpoint: POST /order
    Description: Allows users to create a new order by specifying item and the total amount, deducting the necessary funds from the user's account.
    Responses:
    200: Order created successfully.
    400: Bad request if the request is malformed.
    404: User not found if the user associated with the token is not found.

Get Order List

    Endpoint: GET /order/list
    Description: Retrieves a list of orders associated with the authenticated user.
    Responses:
    200: List of orders associated with the user.
    404: User not found if the user associated with the token is not found.


Running the Services:

1. Build the Docker Images:

```docker-compose build```

2. Run the Docker Containers

```docker-compose up  ```

Testing the Services

```python tests.py```