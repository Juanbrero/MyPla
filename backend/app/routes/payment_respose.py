from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter()

@router.post('/api/mp-notification')
def webhook_mp(data: dict):
    print('MP NOTIFICATION')
    print(data)
    return JSONResponse(status_code= status.HTTP_202_ACCEPTED, content= data)