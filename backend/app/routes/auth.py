from fastapi import APIRouter, Depends, HTTPException
from app.auth0.dependencies import validate_token, RolesValidator
from app.auth0.dependencies import RolesValidator
import json

router = APIRouter()

@router.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}

@router.get("/api/test-professional")
def test_professional (user_info = Depends(RolesValidator(['Profesional']))):
    print(user_info)
    return {"test": "Funciono " + json.dumps(user_info)} 