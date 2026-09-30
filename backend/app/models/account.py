from datetime import datetime
from beanie import Document, PydanticObjectId

class Account(Document):
    user_id: PydanticObjectId
    balance: float
    account_type: str
    created_at: datetime

    class Settings:
        name = "accounts"