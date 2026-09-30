from data import Customers
from database import customer_collection
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

class CustomerRepository:
    async def get_all(self):
        return await customer_collection.find().to_list(length=None)
    
    async def get_by_id(self, customer_id:str):
        try:
            oid = ObjectId(customer_id)
        except InvalidId:
            return None

        return await customer_collection.find_one({"_id" : oid})

    async def get_by_email(self, email:str):
        return await customer_collection.find_one({"email" : email})
    
    async def get_by_email(self, email:str):
        return await customer_collection.find_one({"email" : email})
    
    async def create(self, customer: dict):
        return await customer_collection.insert_one(customer)

    async def update(self, customer_id:str, data:dict):
        try:
            oid = ObjectId(customer_id)
        except InvalidId:
            return None
        await customer_collection.update_one(
            {"_id" : oid},
            {"$set" : data},
        )
        return await customer_collection.find_one({"_id" : oid})

    async def delete(self, customer_id:str):
        try:
            oid = ObjectId(customer_id)
        except InvalidId:
            return None
        result = await customer_collection.delete_one({"_id" : oid})
        return result.deleted_count == 1

customer_repository = CustomerRepository()