from fastapi import FastAPI
from routes.customers import router
from contextlib import asynccontextmanager
from database import client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify MongoDB connection when FastAPI starts
    await client.admin.command("ping")
    print("Connected to MongoDB")

    yield

    # Close MongoDB connection when FastAPI shuts down
    await client.close()
    print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
