from datetime import datetime
from typing import Annotated
from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Transaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    account_id: PyObjectId = Field(serialization_alias="accountId")
    txn_type: str = Field(serialization_alias="txnType")
    amount: float
    created_at: datetime = Field(serialization_alias="createdAt")