from fastapi import FastAPI
from backend.routers import users

app = FastAPI(title="Mesh Alert System", description="API for managing users, alerts and alert nodes", version="1.0.0")

app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}