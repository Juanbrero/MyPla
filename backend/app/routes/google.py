from fastapi import APIRouter, Request
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from googleapiclient.discovery import build

router = APIRouter()

CLIENT_ID = "943184283815-8msdh7njimvd3a77gtnoor5prj9gdnnl.apps.googleusercontent.com"

class TokenData(BaseModel):
    token: str

@router.post("/api/google-auth")
async def google_auth(data: TokenData):
    idinfo = id_token.verify_oauth2_token(data.token, google_requests.Request(), CLIENT_ID)

    user_email = idinfo['email']

    return {"message": "Usuario autenticado", "email": user_email}