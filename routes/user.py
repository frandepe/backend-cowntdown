from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User # esta es la clase User que hemos creado en el archivo schemas/user.py

user = APIRouter()
# Fast instalo la libreria: pip install cryptographys
# Lo que hace es encriptar la contraseñaaa

@user.get("/all-users") # definimos endpoint donde se visualizan los datosaas
def get_users(): # asignamos este nombre a la funcion
    return conn.execute(users.select()).fetchall() # conectamos a la base de datos, consulta con select elegimos la tabla users y con fetchall traemos todos los datos

@user.put("/update-user")
def read_user():
    return {"Hello": "Update"}


@user.post("/create-user")
def create_user(user: User):
    return {"hello": "Create"}

