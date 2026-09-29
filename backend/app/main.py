from fastapi import FastAPI
from routes.customers import router

app = FastAPI()

app.include_router(router)

