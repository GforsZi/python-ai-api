from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.roles import schemas
from app.shared.utils import ApiResponse
from . import service
from app.modules.users.models import User
from app.shared.dependencies import get_current_user

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/")
async def read_role(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.get_all_roles(db)
    return ApiResponse(message="Get all role data", data=data, current_user=current_user)

@router.post("/")
async def add_role(role: schemas.RoleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.create_role(role, db)
    return ApiResponse(message=f"Create new role",data=data, current_user=current_user)

@router.put("/{role_id}")
async def update_existing_role(role_id: int, role: schemas.RoleUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.update_role(role_id, role, db)
    return ApiResponse(message="Update existing role", data=data, current_user=current_user)

@router.delete("/{role_id}")
async def remove_role(role_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.delete_role(role_id, db)
    return ApiResponse(message=f"Delete existing role - {data}", current_user=current_user)

