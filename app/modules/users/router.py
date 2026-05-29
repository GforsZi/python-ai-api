from fastapi import APIRouter
from . import schemas, service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/", response_model=list[schemas.UserResponse])
def read_user():
    return service.get_all_users()

@router.post("/", response_model=schemas.UserResponse)
def add_user(user: schemas.UserCreate):
    return service.create_user(user)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_existing_user(user_id: int, user: schemas.UserCreate):
    return service.update_user(user_id, user)

@router.delete("/{user_id}")
def remove_user(user_id: int):
    return service.delete_user(user_id)

