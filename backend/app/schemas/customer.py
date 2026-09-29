from pydantic import BaseModel


class CreateCustomer(BaseModel):
    id: int
    name: str
    email: str

class UpdatedCustomer(BaseModel):
    name: str
    email: str