from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.schemas import RoleCreate, RoleUpdate
from app.modules.roles.models import Role


async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(Role.id, Role.name, Role.description, Role.is_admin, Role.created_at, Role.updated_at))
    role = result.mappings().all()
    return role

async def create_role(role_data: RoleCreate, db: AsyncSession):
    new_role = Role(name=role_data.name, description=role_data.description, is_admin=role_data.is_admin)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

async def update_role(role_id: int, role_data: RoleUpdate, db: AsyncSession):
    result = await db.execute(select(Role.id).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    update_dict = role_data.model_dump(exclude_unset=True)
    if update_dict:
        await db.execute(
            update(Role).where(Role.id == role_id).values(**update_dict)
        )

    await db.commit()
    update_role = await db.execute(select(Role.id, Role.name, Role.is_admin).where(Role.id == role_id))
    return update_role.mappings().one_or_none()

async def delete_role(role_id: int, db: AsyncSession):
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    await db.delete(role)
    await db.commit()

    return f"role with id {role_id} deleted"

