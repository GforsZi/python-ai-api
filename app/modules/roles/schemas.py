from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: str | None
    is_admin: bool | None = None

class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_admin: bool | None = None
