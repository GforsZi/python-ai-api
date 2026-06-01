from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.models import User
from app.shared.dependencies import get_current_user
from . import schemas, service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/", response_model=list[schemas.UserResponse])
async def read_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data =  await service.get_all_users(db)
    return data

@router.post("/", response_model=schemas.UserResponse)
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_user(user, db)

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_existing_user(user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.update_user(user_id, user, db)

@router.delete("/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await service.delete_user(user_id, db)

