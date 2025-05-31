from fastapi import FastAPI
from routes.user import user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from config.db import conn
from models.user import users
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from routes.yolo import router as yolo_router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

SECRET_KEY2 = os.getenv("SECRET_KEY2")
ALGORITHM2 = os.getenv("ALGORITHM2")
ACCESS_TOKEN_EXPIRE_MINUTES2 = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES2"))  # duración del token en minutos

app = FastAPI()

# --------- CONFIGURACION DE CORS 

origins = [
    "http://localhost:5173",  # tu frontend local, cámbialo según corresponda
    "https://tu-dominio-frontend.com",  # si tienes dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],         # para que acepte OPTIONS, POST, GET, etc
    allow_headers=["*"],
)

# --------------------------------------

# Users
app.include_router(user, prefix="/users", tags=["Users"])

@app.post("/token", tags=["Users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = conn.execute(users.select().where(users.c.email == form_data.username)).mappings().first()
    if not db_user or not bcrypt.checkpw(form_data.password.encode('utf-8'), db_user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES2)
    to_encode = {"sub": db_user["email"], "exp": datetime.utcnow() + access_token_expires}
    access_token = jwt.encode(to_encode, SECRET_KEY2, algorithm=ALGORITHM2)

    return {"access_token": access_token, "token_type": "bearer"}

#Yolo
app.include_router(yolo_router, prefix="/yolo", tags=["Yolo"]) 





