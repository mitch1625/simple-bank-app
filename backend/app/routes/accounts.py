from fastapi import APIRouter, HTTPException
from schemas.account import Account, AmountRequest, CreateAccount
from schemas.transaction import Transaction
from services.account_service import account_service

router = APIRouter(prefix="/api")


@router.post("/accounts", response_model=Account, status_code=201) 
async def create_account(new_account: CreateAccount):
    return await account_service.create_account(
        new_account.user_id, new_account.account_type
    )


@router.get("/accounts/{account_id}", response_model=Account, status_code=200)
async def get_account_by_id(account_id: str):
    account = await account_service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("/users/{user_id}/accounts", response_model=list[Account], status_code=200)
async def get_user_accounts(user_id: str):
    return await account_service.get_all_by_user(user_id)


@router.post("/accounts/{account_id}/deposit", response_model=Account, status_code=200)
async def deposit(account_id: str, body: AmountRequest):
    account = await account_service.deposit(account_id, body.amount)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/accounts/{account_id}/withdraw", response_model=Account, status_code=200)
async def withdraw(account_id: str, body: AmountRequest):
    account = await account_service.withdraw(account_id, body.amount)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found or insufficient funds")
    return account


@router.get(
    "/accounts/{account_id}/transactions",
    response_model=list[Transaction],
    status_code=200,
)
async def get_account_transactions(account_id: str):
    return await account_service.get_transactions(account_id)
