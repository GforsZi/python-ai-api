from fastapi import  HTTPException
import bcrypt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.models import Role
from app.modules.users.models import User
from .schemas import UserCreate, UserUpdate

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User.id, User.username, User.email, User.created_at, User.updated_at, Role.name.label("role_name")).join(User.role))
    raw_user = result.mappings().all()
    formated_user = []
    for user in raw_user:
        user_dict = dict(user)
        user_dict["role"] = {
            "name": user_dict.pop("role_name")
        }
        formated_user.append(user_dict)
    return formated_user

async def create_user(user_data: UserCreate, db: AsyncSession):
    hashed = bcrypt.hashpw(user_data.password[:72].encode(), bcrypt.gensalt()).decode()
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return f"User {new_user.email} created"

async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession):
    result = await db.execute(select(User.id).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = user_data.model_dump(exclude_unset=True)
    if update_dict:
        await db.execute(
            update(User).where(User.id == user_id).values(**update_dict)
        )

    await db.commit()
    update_user = await db.execute(select(User.id, User.username, User.email).where(User.id == user_id))
    return update_user.mappings().one_or_none()

async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return f"User with id {user_id} deleted"
