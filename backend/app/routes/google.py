from fastapi import APIRouter, Request
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from googleapiclient.discovery import build
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow

router = APIRouter()

CLIENT_ID = "943184283815-8msdh7njimvd3a77gtnoor5prj9gdnnl.apps.googleusercontent.com"

class TokenData(BaseModel):
    token: str

@router.post("/api/google-auth")
async def google_auth(data: TokenData):
    idinfo = id_token.verify_oauth2_token(data.token, google_requests.Request(), CLIENT_ID)

    user_email = idinfo['email']

    return {"message": "Usuario autenticado", "email": user_email}

@router.get("/api/login-google")
def login():
    flow = Flow.from_client_secrets_file(
        "/app/app/client_secret_943184283815-8msdh7njimvd3a77gtnoor5prj9gdnnl.apps.googleusercontent.com.json",  # descargado desde Google Cloud
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="http://localhost:8002/api/auth-callback"
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)

@router.get("/api/auth-callback")
def auth_callback(request: Request):
    flow = Flow.from_client_secrets_file(
        "/app/app/client_secret_943184283815-8msdh7njimvd3a77gtnoor5prj9gdnnl.apps.googleusercontent.com.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="http://localhost:8002/api/auth-callback"
    )

    flow.fetch_token(authorization_response=str(request.url))

    credentials = flow.credentials
    service = build("calendar", "v3", credentials=credentials)

    # Crear un evento de ejemplo:
    event = {
        "summary": "Clase sincrónica",
        "start": {"dateTime": "2025-03-28T10:00:00-03:00"},
        "end": {"dateTime": "2025-03-28T11:00:00-03:00"},
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 15}],
        },
    }

    service.events().insert(calendarId='primary', body=event).execute()

    return {"message": "Evento creado y recordatorio activado"}