from fastapi import HTTPException
import bcrypt
from .schemas import UserCreate

db_users = []

def get_password_hash(password: str) -> str:
    password_bytes = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password[:72].encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))

def get_all_users():
    return db_users

def create_user(user_data: UserCreate):
    new_id = len(db_users) + 1
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "id": new_id,
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password
    }
    db_users.append(new_user)
    return new_user

def update_user(user_id: int, user_data: UserCreate):
    for index, user in enumerate(db_users):
        if user["id"] == user_id:
            updated_user = {
                "id": user_id,
                "username": user_data.username,
                "email": user_data.email,
                "hashed_password": get_password_hash(user_data.password)
            }
            db_users[index] = updated_user
            return updated_user

    raise HTTPException(status_code=404, detail="User not found")

def delete_user(user_id: int):
    for index, user in enumerate(db_users):
        if user["id"] == user_id:
            db_users.pop(index)
            return {"message": f"User with ID {user_id} deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
