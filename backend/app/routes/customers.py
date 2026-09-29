from fastapi import APIRouter, HTTPException
from data import Customers
from schemas.customer import CreateCustomer, UpdatedCustomer
from services.customer_service import customer_service

router = APIRouter()


@router.get("/customers", status_code=200)
def get_all_customers():
    return customer_service.get_all()

 
@router.get("/customers/{customer_id}", status_code=200)
def get_customer_by_id(customer_id:int):
    customer = customer_service.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    return customer
    
@router.post("/customers", status_code=201)
def create_customer(new_customer: CreateCustomer):
    ## needs to be updated when db implemented schemas not matching right now
    return customer_service.create(new_customer)


@router.put("/customers/{customer_id}", status_code=200)
def update_customer(customer_id:int, customer: UpdatedCustomer):
    update_customer = customer_service.update(
        customer_id,
        customer.name,
        customer.email
    )
    if update_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return update_customer


@router.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id:int):
    deleted = customer_service.delete(customer_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )