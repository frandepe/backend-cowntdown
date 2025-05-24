from fastapi import APIRouter, Depends
from config.db import conn
from models.user import users
from schemas.user import User
import bcrypt
from libs.utils import get_current_user

user = APIRouter()

@user.post("/create_user")
def create_user(user: User):
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()
        new_user = {"name": user.name, "email": user.email, "password": hashed_password}
        result = conn.execute(users.insert().values(new_user))
        inserted_id = result.inserted_primary_key[0]
        user_created = conn.execute(users.select().where(users.c.id == inserted_id)).mappings().fetchone()
        return user_created
    except Exception as e:
        return {"error": str(e)}

@user.get("/private")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
