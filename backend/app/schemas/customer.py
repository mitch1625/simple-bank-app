from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]
class Customer(BaseModel):
    id: PyObjectId = Field(validation_alias="_id")
    name: str
    email: str

class CreateCustomer(BaseModel):
    name: str
    email: str

class UpdatedCustomer(BaseModel):
    name: str
    email: str