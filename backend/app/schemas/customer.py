from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    name: str
    email: str

class UpdatedCustomer(BaseModel):
    name: str
    email: str