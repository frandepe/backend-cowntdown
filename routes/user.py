# C:\Users\jeroa\Desktop\JeroAlderete\3 - CowntDown Project\backend-cowntdown-main\routes\user.py

from fastapi import APIRouter, Depends, Response
from schemas.user import User
import bcrypt
from libs.utils import get_current_user
from libs.utils import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends
from config.db import supabase

user = APIRouter()

@user.post("/create_user")
def create_user(user_data: User):  # Usa tu esquema Pydantic User si tienes
    # Primero validar que email no exista
    existing = supabase.table('users').select('*').eq('email', user_data.email).execute()
    if existing.data and len(existing.data) > 0:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode()
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password
    }
    result = supabase.table('users').insert(new_user).execute()
    if not result.data or len(result.data) == 0:
        raise HTTPException(status_code=500, detail="Error al insertar el usuario")
    return result.data[0]  # Retornar el usuario insertado


@user.get("/private")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


@user.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        result = supabase.table('users').select('*').eq('email', form_data.username).execute()
        # print("Supabase query result raw:", result)
        # print("Result dir:", dir(result))

        # Verificar datos
        if not hasattr(result, "data") or result.data is None or len(result.data) == 0:
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

        user = result.data[0]

        if "password" not in user:
            raise HTTPException(status_code=500, detail="Usuario sin contraseña en la base")

        password_matches = bcrypt.checkpw(
            form_data.password.encode('utf-8'),
            user["password"].encode('utf-8')
        )
        if not password_matches:
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

        access_token = create_access_token(data={"sub": user["email"]})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60*60*24
        )

        return {"message": "Login exitoso"}

    except HTTPException as e:
        raise e
    except Exception as e:
        # import traceback
        # print("Traceback error completo:")
        # traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@user.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return {"message": "Logout exitoso"}