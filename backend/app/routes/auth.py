from fastapi import APIRouter, Depends, HTTPException
from app.auth0.dependencies import validate_token
from app.auth0.set_user_type import UserTypePayload
from app.auth0.management import get_management_token
from app.auth0.config import settings
import os
import requests

router = APIRouter()

@router.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}


@router.post("/api/user/type")
def set_user_type(payload: UserTypePayload):
    mgmt_token = get_management_token()

    print(payload.tipo_usuario)
    print(payload.user_id)

    url = f"https://{settings.auth0_domain}/api/v2/users/{payload.user_id}"
    headers = {
        "Authorization": f"Bearer {mgmt_token}",
        "Content-Type": "application/json"
    }
    data = {
        "user_metadata": {
            "tipo_usuario": payload.tipo_usuario
        }
    }

    response = requests.patch(url, json=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"message": "User type updated"}