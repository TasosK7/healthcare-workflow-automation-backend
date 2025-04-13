from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running!"}

app.include_router(api_router)

