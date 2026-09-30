from datetime import datetime
from beanie import Document, PydanticObjectId


class Transaction(Document):
    account_id: PydanticObjectId
    txn_type: str
    amount: float
    created_at: datetime

    class Settings:
        name = "transactions"