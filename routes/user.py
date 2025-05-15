from fastapi import APIRouter
from config.db import conn
from models.user import users

user = APIRouter()
# Fast instalo la libreria: pip install cryptography
# Lo que hace es encriptar la contraseña
@user.get("/all-users")
def get_users():
    return conn.execute(users.select()).fetchall()

@user.put("/update-user")
def read_user():
    return {"Hello": "Update"}