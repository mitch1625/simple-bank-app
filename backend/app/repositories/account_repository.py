from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from database import account_collection


def _to_oid(value: str):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None

class AccountRepository:
    async def create(self, user_id: str, account_type: str, balance: float):
        doc = {
            "user_id": ObjectId(user_id),
            "account_type": account_type,
            "balance": round(balance, 2),
            "created_at": datetime.now(timezone.utc),
        }
        result = await account_collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def get_by_id(self, account_id: str):
        oid = _to_oid(account_id)
        if oid is None:
            return None
        return await account_collection.find_one({"_id": oid})

    async def get_all_by_user(self, user_id: str):
        oid = _to_oid(user_id)
        if oid is None:
            return []
        return await account_collection.find({"user_id": oid}).to_list(length=None)

    async def increase_balance(self, account_id: str, amount: float):
        """Atomic add. Returns the updated doc, or None if the account doesn't exist."""
        oid = _to_oid(account_id)
        if oid is None:
            return None
        return await account_collection.find_one_and_update(
            {"_id": oid},
            {"$inc": {"balance": round(amount, 2)}},
            return_document=ReturnDocument.AFTER,
        )

    async def decrease_balance_if_sufficient(self, account_id: str, amount: float):
        """Atomic subtract that only applies if balance >= amount.
        Returns the updated doc, or None if the account is missing or funds are short."""
        oid = _to_oid(account_id)
        if oid is None:
            return None
        return await account_collection.find_one_and_update(
            {"_id": oid, "balance": {"$gte": amount}},
            {"$inc": {"balance": -round(amount, 2)}},
            return_document=ReturnDocument.AFTER,
        )


account_repository = AccountRepository()
