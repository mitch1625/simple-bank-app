import os
from beanie import init_beanie
from fastapi import FastAPI
from routes.users import router as users_router
from routes.accounts import router as accounts_router
from contextlib import asynccontextmanager
from models.user import User
from models.account import Account
from models.transaction import Transaction
from database import client, db
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify MongoDB connection when FastAPI starts
    await client.admin.command("ping")
    print("Connected to MongoDB")

    await init_beanie(database=db, document_models=[User, Account, Transaction])
    
    yield

    # Close MongoDB connection when FastAPI shuts down
    if not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        await client.close()
        print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(accounts_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)