from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status
from app.controllers.ReservationController import ReservationController
from sqlalchemy.orm import Session
from app.config.database import get_db
import mercadopago 
from os import getenv

sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))

router = APIRouter()

@router.post('/api/mp-notification')
def webhook_mp(data: dict, db: Session = Depends(get_db)):
    print('MP NOTIFICATION')
    print(data)

    payment_id = data['data']['id']
    payment_response = sdk.payment().get(payment_id)
    payment_data = payment_response["response"]

    # Extraés la metadata
    metadata = payment_data.get("metadata", {})
    student_id = metadata.get("student_id")
    statusP = payment_data.get("status")
    print(f'STATUS: {statusP}')

    if statusP in ["approved", "rejected", "cancelled"]:
        ReservationController(db= db).updatePay(student_id= student_id, statusP= statusP)

    

    return JSONResponse(status_code= status.HTTP_200_OK, content= '')