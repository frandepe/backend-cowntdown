from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.db import conn
from models.user import users
from datetime import datetime, timedelta # libreria para manipular fechas horas etc
import os
from dotenv import load_dotenv

load_dotenv()

# Variables necesarias para el JWT
SECRET_KEY1 = os.getenv("SECRET_KEY1")
ALGORITHM1 = os.getenv("ALGORITHM1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
ACCESS_TOKEN_EXPIRE_MINUTES1 = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES1")) # duración del token en minutos

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token inválido",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         user = conn.execute(users.select().where(users.c.email == email)).mappings().first()
#         if user is None:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")
#         return user
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token inválido",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


def get_current_user(request: Request):
    token = request.cookies.get("access_token")  # sacar token de la cookie
    print("🔍 TOKEN DESDE COOKIE:", token)  # << este log es clave

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado, token no encontrado en cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY1, algorithms=[ALGORITHM1])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = conn.execute(users.select().where(users.c.email == email)).mappings().first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token(data: dict): # en data almacenamos datos como el usuario o el email
    to_encode = data.copy() # creamos una copia del dato para poder modificarlo
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES1) # calculamos el tiempo de expiracion del token
    
    to_encode.update({"exp": expire}) # agregamos la clave de expiracion al payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY1, algorithm=ALGORITHM1) # codificamos el token jwt
    
    print("✅ DATETIME EXP:", expire)
    print("✅ PAYLOAD JWT:", to_encode)
    print("✅ JWT TOKEN:", encoded_jwt)
    return encoded_jwt # retornamos el jwt codificado