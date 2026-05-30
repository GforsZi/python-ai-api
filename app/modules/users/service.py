from fastapi import  HTTPException
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from .schemas import UserCreate, UserUpdate

db_users = []

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    user = result.scalars().all()
    return user

async def create_user(user_data: UserCreate, db: AsyncSession):
    hashed = bcrypt.hashpw(user_data.password[:72].encode(), bcrypt.gensalt()).decode()
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"Message": f"User {user_id} deleted"}
