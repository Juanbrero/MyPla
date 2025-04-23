from fastapi import APIRouter, Depends, HTTPException
from app.auth0.dependencies import validate_token

router = APIRouter()

@router.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}

