#C:\Users\jeroa\Desktop\JeroAlderete\3 - CowntDown Project\backend-cowntdown-main\libs\utils.py

from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta # libreria para manipular fechas horas etc
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from config.db import supabase  

load_dotenv()

# Variables necesarias para el JWT
SECRET_KEY1 = os.getenv("SECRET_KEY1")
ALGORITHM1 = os.getenv("ALGORITHM1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
ACCESS_TOKEN_EXPIRE_MINUTES1 = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES1")) # duración del token en minutos

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
        
        # Aquí hacemos la consulta a supabase para obtener el usuario
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.error:
            raise HTTPException(status_code=500, detail="Error al consultar usuario")
        
        user_list = response.data
        if not user_list:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user = user_list[0]  # asumiendo que email es único y retorna lista
        
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