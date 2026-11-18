from fastapi import FastAPI
from backend.api.routers import users
from api.routers.alerts import router as alert_router

app = FastAPI(title="Mesh Alert System", description="API for managing users, alerts and alert nodes", version="1.0.0")

app.include_router(alert_router)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}