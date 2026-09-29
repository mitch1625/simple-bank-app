from pydantic import BaseModel


class Transactions(BaseModel):
    account_id: int
    txn_type: str
    amount: float
    created_at: str
    