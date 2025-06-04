#C:\Users\jeroa\Desktop\JeroAlderete\3 - CowntDown Project\backend-cowntdown-main\routes\auth_google.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import supabase
from libs.oauth import oauth
from config.settings import settings
from libs.utils import create_access_token
from supabase import create_client, Client

url = "https://xnbukikosdcaggqnvybb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhuYnVraWtvc2RjYWdncW52eWJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODk5NjI0NywiZXhwIjoyMDY0NTcyMjQ3fQ.xCfoKXgkYrP9yoVABNBJCdkqr1fN1mnAjneBTvQiy3A"

supabase: Client = create_client(url, key)


router = APIRouter()

@router.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)



# creamos el usuario cuando ingresa por google en la bd
def get_or_create_user(user_info):
    google_id = user_info["sub"]

    # 1. Buscar usuario por su Google ID
    result = supabase.table("users").select("*").eq("google_id", google_id).execute()

    if result.data:
        return result.data[0]  # Usuario ya existe

    # 2. Si no existe, lo creamos
    new_user = {
        "google_id": google_id,
        "email": user_info["email"],
        "username": user_info.get("username") or user_info["email"].split("@")[0],
        "email_verified": user_info.get("email_verified", False),
    }

    insert_result = supabase.table("users").insert(new_user).execute()
    return insert_result.data[0]


@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    # Buscar o crear al usuario en tu DB
    user = get_or_create_user(user_info)

    # Crear el JWT
    jwt_token = create_access_token({"sub": user["id"]})

    # return JSONResponse(content={"access_token": jwt_token, "user": user})
    # En lugar de devolver el JSON, haces:
    return RedirectResponse(url="http://localhost:5173/upload-video")  # o la URL que quieras
