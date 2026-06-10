from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from app.core.database import get_db
from app.modules.users.models import User
from app.shared.dependencies import get_current_user
from app.shared.utils import ApiResponse
from . import schemas, service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/")
async def read_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data =  await service.get_all_users(db)
    return ApiResponse(message="Get all user data", data=data, current_user=current_user)

@router.post("/")
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.create_user(user, db)
    return ApiResponse(message=f"Create new user - {data}", current_user=current_user)

@router.put("/{user_id}")
async def update_existing_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    data = await service.update_user(user_id, user, db)
    return ApiResponse(message="Update existing user", data=data, current_user=current_user)

@router.delete("/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)):
    data = await service.delete_user(user_id, db)
    return ApiResponse(message=f"Delete existing user - {data}", current_user=current_user)

