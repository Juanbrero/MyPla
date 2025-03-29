from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from os import getenv

router = APIRouter()

config_data = {
    'GOOGLE_CLIENT_ID': getenv("GOOGLE_CLIENT_ID"),
    'GOOGLE_CLIENT_SECRET': getenv("GOOGLE_CLIENT_SECRET"),
}
config = Config(environ=config_data)

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=getenv("GOOGLE_CLIENT_ID"),
    client_secret=getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get('/login')
async def login(request: Request):
    redirect_uri = 'http://localhost:3000/oauth-callback'
    resAuth = await oauth.google.authorize_redirect(request, redirect_uri)
    return resAuth

@router.get('/auth')
async def auth(request: Request):
    print(request)
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if not user_info:
        # Si no viene en userinfo, intenta obtenerla manualmente
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        user_info = resp.json()
    return {"token": token, "user": user_info}