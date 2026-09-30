from fastapi import APIRouter, HTTPException
from schemas.customer import CreateCustomer, UpdatedCustomer
from services.customer_service import customer_service
from schemas.customer import Customer

router = APIRouter()


@router.get("/customers", response_model=list[Customer], status_code=200)
async def get_all_customers():
    return await customer_service.get_all()

 
@router.get("/customers/{customer_id}", response_model=Customer, status_code=200)
async def get_customer_by_id(customer_id:str):
    customer = await customer_service.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    return customer

@router.post("/customers", status_code=201)
async def create_customer(new_customer: CreateCustomer):
    return await customer_service.create(new_customer)


@router.put("/customers/{customer_id}", response_model=Customer,status_code=200)
async def update_customer(customer_id:str, customer: UpdatedCustomer):
    updated = await customer_service.update(customer_id, customer)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return updated


@router.delete("/customers/{customer_id}", status_code=204)
async def delete_customer(customer_id:str):
    deleted = await customer_service.delete(customer_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )