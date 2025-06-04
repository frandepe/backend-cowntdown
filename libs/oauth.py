# from authlib.integrations.starlette_client import OAuth
# from config.settings import settings

# oauth = OAuth()

# oauth.register(
#     name='google',
#     client_id=settings.google_client_id,
#     client_secret=settings.google_client_secret,
#     access_token_url='https://oauth2.googleapis.com/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     client_kwargs={'scope': 'openid email profile'},
# )


from authlib.integrations.starlette_client import OAuth
from config.settings import settings

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    }
)
