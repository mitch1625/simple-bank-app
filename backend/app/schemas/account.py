from pydantic import BaseModel

class Account(BaseModel):
    balance: float
    account_type: str
    created_at: str