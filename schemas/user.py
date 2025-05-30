# usamos pydantic desde fastapi que nos permite agregar tipo de datos, Basemodel te permite crear un modelo de datos
from pydantic import BaseModel
# es la forma de importar un tipo de dato, en este caso un dato opcional
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str
