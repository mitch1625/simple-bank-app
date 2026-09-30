from repositories.customer_repository import customer_repository
from schemas.customer import CreateCustomer, UpdatedCustomer
from fastapi import HTTPException

class CustomerService:

    async def get_all(self):
        return await customer_repository.get_all()

    async def get_by_id(self, customer_id: str):
        return await customer_repository.get_by_id(customer_id)


    async def create(self, new_customer: CreateCustomer):
        existing_customer = await customer_repository.get_by_email(new_customer.email)
        if existing_customer:
            raise HTTPException(
                status_code=409,
                detail="Customer with that email already exists"
            )
        await customer_repository.create(new_customer.model_dump())
        return {"message" : "Customer created"}

    async def update(self, customer_id: str, data: UpdatedCustomer):
        customer = await customer_repository.get_by_id(customer_id)

        if customer is None:
            return None
        existing_email = await customer_repository.get_by_email(data.email)
        if existing_email and str(existing_email["_id"]) != customer_id:
            raise HTTPException(
                status_code=409,
                detail="Cannot use duplicate emails"
            )
        return await customer_repository.update(customer_id, data.model_dump())

    
    async def delete(self, customer_id: str):
        customer = await customer_repository.get_by_id(customer_id)
        print(customer)
        if customer is None:
            return None
        return await customer_repository.delete(customer_id)
        

customer_service = CustomerService()