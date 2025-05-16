from fastapi import APIRouter
from config.db import conn
from models.user import users

user = APIRouter()
# Fast instalo la libreria: pip install cryptography
# Lo que hace es encriptar la contraseñaaa

@user.get("/all-users") # definimos endpoint donde se visualizan los datosaa
def get_users(): # asignamos este nombre a la funcion
    return conn.execute(users.select()).fetchall() # conectamos a la base de datos, consulta con select elegimos la tabla users y con fetchall traemos todos los datos

@user.put("/update-user")
def read_user():
    return {"Hello": "Update"}


