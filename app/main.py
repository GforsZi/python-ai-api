from fastapi import FastAPI, HTTPException
from app.modules.users.router import router as user_router
app = FastAPI(title="Modular API")

app.include_router(user_router)

users = []

@app.get("/")
def root():
    return {"message": "Welcome to my api project"}

