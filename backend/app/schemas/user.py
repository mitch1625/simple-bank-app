from typing import Annotated
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: PyObjectId = Field(validation_alias="_id")
    name: str
    email: str


class CreateUser(BaseModel):
    name: str
    email: str


class UpdatedUser(BaseModel):
    name: str
    email: str