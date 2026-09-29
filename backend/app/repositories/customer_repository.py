from data import Customers

class CustomerRepository:
    def get_all(self):
        return Customers

    def get_by_id(self, customer_id:int):
        return Customers.get(customer_id)

    def create(self, customer: dict):
        Customers[customer["id"]] = customer

    def update(self, customer_id:int, customer:dict):
        Customers[customer_id] = customer

    def delete(self, customer_id:int):
        del Customers[customer_id]


customer_repository = CustomerRepository()