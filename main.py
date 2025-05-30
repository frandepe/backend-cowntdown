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


SECRET_KEY = "secret_key_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

app = FastAPI()
# Users
app.include_router(user, prefix="/users", tags=["Users"])

@app.post("/token", tags=["Users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = conn.execute(users.select().where(users.c.email == form_data.username)).mappings().first()
    if not db_user or not bcrypt.checkpw(form_data.password.encode('utf-8'), db_user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": db_user["email"], "exp": datetime.utcnow() + access_token_expires}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}

#Yolo
app.include_router(yolo_router, prefix="/yolo", tags=["Yolo"]) 
