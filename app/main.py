from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.modules.users.router import router as user_router
from app.modules.chatbots.router import router as chat_router
from app.modules.auth.router import router as auth_router
app = FastAPI(title="Modular API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="My API",
        version="1.0.0",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Welcome to my api project"}

