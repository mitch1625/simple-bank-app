from beanie import init_beanie
from fastapi import FastAPI
from routes.users import router as users_router
from routes.accounts import router as accounts_router
from contextlib import asynccontextmanager
from models.user import User
from models.account import Account
from models.transaction import Transaction
from database import client, db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify MongoDB connection when FastAPI starts
    await client.admin.command("ping")
    print("Connected to MongoDB")

    await init_beanie(database=db, document_models=[User, Account, Transaction])
    
    yield

    # Close MongoDB connection when FastAPI shuts down
    await client.close()
    print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(accounts_router)