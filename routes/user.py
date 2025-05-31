# C:\Users\jeroa\Desktop\JeroAlderete\3 - CowntDown Project\backend-cowntdown-main\routes\user.py

from fastapi import APIRouter, Depends, Response
from config.db import conn
from models.user import users
from schemas.user import User
import bcrypt
from libs.utils import get_current_user
from libs.utils import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends

user = APIRouter()


@user.post("/create_user")
def create_user(user: User):
    try:
        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'), bcrypt.gensalt()).decode()
        new_user = {"name": user.name, "email": user.email,
                    "password": hashed_password}
        result = conn.execute(users.insert().values(new_user))
        inserted_id = result.inserted_primary_key[0]
        user_created = conn.execute(users.select().where(
            users.c.id == inserted_id)).mappings().fetchone()
        return user_created
    except Exception as e:
        return {"error": str(e)}


@user.get("/private")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


# @user.post("/login")

# # OAuth2PasswordRequestForm  extraer y valida los datos enviados en el formulario
# def login(form_data: OAuth2PasswordRequestForm = Depends()): # Depends() indica que FastAPI debe "inyectar" esos datos usando la clase OAuth2PasswordRequestForm.
#     # Buscar usuario en la base de datos por email (form_data.username es el email)
#     user = conn.execute(users.select().where(users.c.email == form_data.username)).mappings().fetchone()
#     # validacion si no matchea
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos") # httpexception lanzar errores HTTP desde los endpoints.

#     # Verificar match contraseña
#     if not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos") #

#     # Crear token JWT access token (sucede desde nuestra función creada)
#     access_token = create_access_token(data={"sub": user["email"]})

#     return {"access_token": access_token, "token_type": "bearer"}

@user.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario en la base de datos por email
    user = conn.execute(users.select().where(
        users.c.email == form_data.username)).mappings().fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Email o contraseña incorrectos")

    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Email o contraseña incorrectos")

    access_token = create_access_token(data={"sub": user["email"]})

    # Seteamos la cookie HttpOnly para el token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Cambiar a True si usas HTTPS en producción
        samesite="lax",  # o "strict" según necesites
        max_age=60*60*24  # 1 día en segundos
    )

    return {"message": "Login exitoso"}


@user.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,       # Usá True en producción
        samesite="strict",
        path="/"
    )
    return {"message": "Logout exitoso"}
