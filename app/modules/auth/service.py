from fastapi import HTTPException
from app.shared.utils import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.modules.users.models import User
import httpx
import os

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] =  datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

def get_github_auth_url() -> str:
    return (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={APP_URL}/auth/callback"
        f"&scope=user:email"
    )

async def exchange_github_code(code: str) -> dict | None:
    async with httpx.AsyncClient(timeout=30.0) as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": f"{APP_URL}/auth/callback"
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_res.json()
        github_token = token_data.get("access_token")

        if not github_token:
            return None
        
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {github_token}"}
        )
        github_user = user_res.json()

        if not github_user.get("email"):
            email_res = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {github_token}"}
            )

            emails = email_res.json()
            primary = next((e["email"] for e in emails if e["primary"]), None)
            github_user["email"] = primary

        return github_user

async def github_login(db: AsyncSession, code: str):
    github_user = await exchange_github_code(code)

    if not github_user:
        return ApiResponse(
            message="Failed to authenticate with GitHub",
            status_code=400
        ).to_dict()

    github_id = str(github_user["id"])
    email = github_user.get("email", "")
    username = github_user.get("login", "")
    avatar_url = github_user.get("avatar_url", "")

    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalar_one_or_none()

    if not user:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user:
            user.github_id = github_id
            user.avatar_url = avatar_url
        else:
            user = User(
                username=username,
                email=email,
                github_id=github_id,
                avatar_url=avatar_url,
                hashed_password=None
            )
            db.add(user)

        await db.commit()
        await db.refresh(user)

    access_token = create_access_token({"sub": str(user.id), "email": user.email})

    return ApiResponse(
        message="Login successful",
        data={"access_token": access_token, "token_type": "bearer"}
    ).to_dict()
