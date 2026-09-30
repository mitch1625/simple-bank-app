import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncMongoClient(MONGODB_URI)

db = client["bank-app"]

user_collection = db["users"]
account_collection = db["accounts"]
transaction_collection = db["transactions"]