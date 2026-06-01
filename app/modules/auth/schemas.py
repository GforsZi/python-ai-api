from pydantic import BaseModel


class TokenRespone(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRespone(BaseModel):
    id: int
    username: str
    email: str
    github_id: str | None = None
    avatar_url: str | None = None

    model_config = {"from_attributes": True}
