from fastapi import FastAPI
from api.requirements import router

app = FastAPI()

app.include_router(router, prefix="/api")