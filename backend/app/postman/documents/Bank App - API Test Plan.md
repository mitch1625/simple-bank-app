# Bank App — API Test Plan

This document describes the full set of API routes for the Bank App backend, the Postman requests that test them, and the recommended collection run order.

---

## Environment Variables

| Variable | Description | Set By |
|---|---|---|
| `baseUrl` | Base URL of the running server (default: `http://localhost:8000`) | Manual |
| `userId` | MongoDB ObjectId of the test user | `Create User` afterResponse script |
| `accountId` | MongoDB ObjectId of the test account | `Create Account` afterResponse script |
| `accountBalance` | Current balance of the test account | `Deposit` / `Withdraw` afterResponse scripts |

---

## User Routes (`/api/users`)

### 1. Create User
- **Method:** `POST`
- **URL:** `{{baseUrl}}/api/users`
- **Body:** `{ "name": "John Doe", "email": "john.doe@example.com" }`
- **Expected Status:** `201`
- **Tests:**
  - Status is 201
  - Response has `id`, `name`, `email`
  - `name` equals `"John Doe"`
  - `email` equals `"john.doe@example.com"`
  - Saves `userId` to environment

### 2. Get All Users
- **Method:** `GET`
- **URL:** `{{baseUrl}}/api/users`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response is an array
  - Each user has `id`, `name`, `email`

### 3. Get User by ID
- **Method:** `GET`
- **URL:** `{{baseUrl}}/api/users/{{userId}}`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response has `id`, `name`, `email`
  - `id` matches `userId` environment variable

### 4. Update User
- **Method:** `PUT`
- **URL:** `{{baseUrl}}/api/users/{{userId}}`
- **Body:** `{ "name": "Jane Doe", "email": "jane.doe@example.com" }`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response has `id`, `name`, `email`
  - `name` equals `"Jane Doe"`

### 5. Delete User
- **Method:** `DELETE`
- **URL:** `{{baseUrl}}/api/users/{{userId}}`
- **Expected Status:** `204`
- **Tests:**
  - Status is 204
  - Response body is empty

---

## Account Routes (`/api/accounts`)

### 6. Create Account
- **Method:** `POST`
- **URL:** `{{baseUrl}}/api/accounts`
- **Body:** `{ "userId": "{{userId}}", "accountType": "checking" }`
- **Expected Status:** `201`
- **Tests:**
  - Status is 201
  - Response has `id`, `userId`, `balance`, `accountType`, `createdAt`
  - `accountType` equals `"checking"`
  - `balance` starts at `0`
  - Saves `accountId` to environment

### 7. Get Account by ID
- **Method:** `GET`
- **URL:** `{{baseUrl}}/api/accounts/{{accountId}}`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response has `id`, `userId`, `balance`, `accountType`, `createdAt`
  - `id` matches `accountId` environment variable

### 8. Get User Accounts
- **Method:** `GET`
- **URL:** `{{baseUrl}}/api/users/{{userId}}/accounts`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response is an array
  - Each account has `id`, `userId`, `balance`, `accountType`, `createdAt`
  - All accounts belong to the correct `userId`

### 9. Deposit
- **Method:** `POST`
- **URL:** `{{baseUrl}}/api/accounts/{{accountId}}/deposit`
- **Body:** `{ "amount": 500.00 }`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response has `id`, `userId`, `balance`, `accountType`, `createdAt`
  - Balance is at least `500`
  - Saves `accountBalance` to environment

### 10. Withdraw
- **Method:** `POST`
- **URL:** `{{baseUrl}}/api/accounts/{{accountId}}/withdraw`
- **Body:** `{ "amount": 100.00 }`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response has `id`, `userId`, `balance`, `accountType`, `createdAt`
  - Balance decreased by `100` from previous `accountBalance`
  - Saves updated `accountBalance` to environment

### 11. Get Account Transactions
- **Method:** `GET`
- **URL:** `{{baseUrl}}/api/accounts/{{accountId}}/transactions`
- **Expected Status:** `200`
- **Tests:**
  - Status is 200
  - Response is an array
  - Each transaction has `id`, `accountId`, `amount`, `type`, `createdAt`
  - Transaction `type` is either `"deposit"` or `"withdrawal"`

---

## Recommended Collection Run Order

Run requests in this order so that environment variables are populated before they are needed:

1. Create User
2. Get All Users
3. Get User by ID
4. Update User
5. Create Account
6. Get Account by ID
7. Get User Accounts
8. Deposit
9. Withdraw
10. Get Account Transactions
11. Delete User

> **Note:** Delete User is placed last to keep `userId` valid throughout the run.
