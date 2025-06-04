from typing import ClassVar, Dict

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = "http://127.0.0.1:8000/auth/google/callback"
    server_metadata_url: ClassVar[str] = 'https://accounts.google.com/.well-known/openid-configuration'
    client_kwargs: ClassVar[dict] = {
        'scope': 'openid email profile',
    }
    access_token_expire_minutes1: int
    access_token_expire_minutes2: int
    algorithm1: str
    supabase_url: str
    supabase_key: str            # <--- agregalo aquí
    supabase_bucket: str
    secret_key1: str
    secret_key2: str


settings = Settings()
