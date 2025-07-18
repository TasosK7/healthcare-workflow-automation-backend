from fastapi import FastAPI
from app.api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:9000"
]
@app.get("/")
def root():
    return {"message": "Backend is running!"}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

