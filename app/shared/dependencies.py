from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.service import decode_access_token
from app.core.database import get_db
from app.modules.roles.models import Role
from app.modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
def get_current_user(allowed_roles: list[str] | None = None):
    async def dependency(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        result = await db.execute(
            select(User.id, User.username, User.email, Role.name.label("role_name"))
            .where(User.id == int(payload["sub"]))
            .join(User.role)
        )
        user = result.mappings().one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if allowed_roles and user.role_name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user
    return dependency
