from repositories.customer_repository import customer_repository
from schemas.customer import CreateCustomer, UpdatedCustomer

class CustomerService:

    def get_all(self):
        return customer_repository.get_all()

    def get_by_id(self, customer_id: int):
        customer = customer_repository.get_by_id(customer_id)
        return customer

    def create(self, new_customer: CreateCustomer):
        ### This is wrong b/c DB implementation not done yet. Schema will change
        existing_customer = customer_repository.get_by_id(new_customer.id)
        if existing_customer:
            raise ValueError("Customer with that email already exists")

        customer_repository.create(new_customer.model_dump())
        return {"message" : "Customer created"}

    def update(self, customer_id: int, name: str, email: str):
        customer = customer_repository.get_by_id(customer_id)

        if customer is None:
            return None
        customer['name'] = name
        customer['email'] = email

        customer_repository.update(customer_id, customer)
        return customer
    
    def delete(self, customer_id: int):
        customer = customer_repository.get_by_id(customer_id)
        if customer is None:
            return None
        customer_repository.delete(customer_id)
        return True

customer_service = CustomerService()