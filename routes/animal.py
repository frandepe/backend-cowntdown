# routes vendria a ser como la carpeta api
from fastapi import APIRouter
from models.animal import animals
from config.db import conn

# definimos el router
animal = APIRouter()

# este vendria a ser el endpoint!!!!
@animal.get("/all-animals")
def get_animals():
    return conn.execute(animals.select()).fetchall()

@animal.put("/update-animals")
def read_animals():
    return{"animalsUpdated"}