from fastapi import FastAPI
from app.api.analysis import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}