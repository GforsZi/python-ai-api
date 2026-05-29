from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.modules.chatbots.router import router as chat_router
app = FastAPI(title="Modular API")

app.include_router(user_router)
app.include_router(chat_router)

users = []

@app.get("/")
def root():
    return {"message": "Welcome to my api project"}

