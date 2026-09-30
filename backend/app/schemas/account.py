from datetime import datetime
from typing import Annotated
from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Account(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    user_id: PyObjectId = Field(
        validation_alias=AliasChoices("user_id", "userId"),
        serialization_alias="userId",
    )
    balance: float
    account_type: str = Field(serialization_alias="accountType")
    created_at: datetime = Field(serialization_alias="createdAt")


class CreateAccount(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(
        validation_alias=AliasChoices("userId", "user_id"),
        pattern=r"^[0-9a-fA-F]{24}$",
        description="The existing user's MongoDB ObjectId",
    )
    account_type: str = Field(
        validation_alias=AliasChoices("accountType", "account_type")
    )


class AmountRequest(BaseModel):
    amount: float