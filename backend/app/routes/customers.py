from fastapi import APIRouter, HTTPException
from data import Customers
from schemas.customer import Customer, UpdatedCustomer

router = APIRouter()

def get_customer_or_404(customer_id:int):
    customer = Customers.get(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=404, detail="Customer not found")
    return customer

@router.get("/customers", status_code=200)
def get_all_customers():
    return Customers
 
@router.get("/customers/{customer_id}", status_code=200)
def get_customer_by_id(customer_id:int):
    return get_customer_or_404(customer_id)

@router.post("/customers", status_code=201)
def create_customer(new_customer: Customer):
    if new_customer.id in Customers:
        raise HTTPException(
            status_code=409,
            detail="Customer with that email already exists")
    Customers[new_customer.id] = new_customer.model_dump()
    return {"message" : "Customer created"}

@router.put("/customers/{customer_id}", status_code=200)
def edit_customer(customer_id:int, updated_customer: UpdatedCustomer):
    customer = get_customer_or_404(customer_id)
    customer['name'] = updated_customer.name
    customer['email'] = updated_customer.email
    return {"message" : "Customer updated successfully"}

@router.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id:int):
    get_customer_or_404(customer_id)
    del Customers[customer_id]
    return {"message" : "Customer deleted successfully"}
