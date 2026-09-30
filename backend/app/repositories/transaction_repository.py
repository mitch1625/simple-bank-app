from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from database import transaction_collection


class TransactionRepository:
    async def create(self, account_id: ObjectId, txn_type: str, amount: float):
        transaction = {
            "account_id": account_id,
            "txn_type": txn_type,
            "amount": round(amount, 2),
            "created_at": datetime.now(timezone.utc),
        }
        result = await transaction_collection.insert_one(transaction)
        transaction["_id"] = result.inserted_id
        return transaction

    async def get_by_account(self, account_id: str):
        try:
            account_oid = ObjectId(account_id)
        except (InvalidId, TypeError):
            return []

        return await (
            transaction_collection.find({"account_id": account_oid}).to_list(length=None)
        )


transaction_repository = TransactionRepository()