import math
from fastapi import HTTPException
from repositories.account_repository import account_repository
from repositories.transaction_repository import transaction_repository
from repositories.user_repository import user_repository


class AccountService:
    async def create_account(self, user_id: str, account_type: str):
        if not account_type.strip():
            raise HTTPException(status_code=400, detail="Account type is required")
        user = await user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return await account_repository.create(user_id, account_type, 0)

    async def get_account(self, account_id: str):
        return await account_repository.get_by_id(account_id)

    async def get_all_by_user(self, user_id: str):
        return await account_repository.get_all_by_user(user_id)

    @staticmethod
    def _validated_amount(amount: float) -> float:
        if not math.isfinite(amount) or round(amount, 2) <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be a positive value of at least 0.01",
            )
        return round(amount, 2)

    async def deposit(self, account_id: str, amount: float):
        amount = self._validated_amount(amount)
        account = await account_repository.increase_balance(account_id, amount)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        await transaction_repository.create(
            account["_id"], "deposit", amount
        )
        return account

    async def withdraw(self, account_id: str, amount: float):
        amount = self._validated_amount(amount)
        existing_account = await account_repository.get_by_id(account_id)
        if existing_account is None:
            raise HTTPException(status_code=404, detail="Account not found")

        account = await account_repository.decrease_balance_if_sufficient(
            account_id, amount
        )
        if account is None:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        await transaction_repository.create(
            account["_id"], "withdrawal", amount
        )
        return account

    async def get_transactions(self, account_id: str):
        if await self.get_account(account_id) is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return await transaction_repository.get_by_account(account_id)


account_service = AccountService()