from sqlalchemy.orm import Session
from app.models import Reservation, Meeting, Class
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic
from datetime import datetime, timedelta
# SDK de Mercado Pago
from os import getenv
import mercadopago
# Agrega credenciales (private key)
sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))


class MPInitialService:
    @handle_errors
    def run (
        reservationR: Repository[Reservation],
        meetingR: Repository[Meeting],
        classR: Repository[Class],
        student_id: str
    ):
        reservations = reservationR.get_by({
            "student_id": student_id,
            "state": "pending"
        })
        
        if (len(reservations) <= 0):
            raise NotFound("User not have a pending pay")
        
        r = reservations[0]
        
        classes = classR.get_by({
            "prof_id": r.prof_id,
            "day_hour": r.day_hour
        })
        if (len(classes) <= 0):
            raise NotFound("Not exist class to pay")
        
        c = classes[0]

        if (datetime.now() - r.create > timedelta(minutes=3)):
            reservationR.delete({
                "student_id": student_id,
                "day_hour": r.day_hour,
                "state": "pending"
            })
            meetingR.delete({
                "prof_id": r.day_hour,
                "day_hour": r.day_hour,
            })
            raise ValidationError("Expired you reservation")
        
        preference_data = {
            "items": [
                {
                    "title": "Pago de reserva en MIPLA",
                    "quantity": 1,
                    "unit_price": c.price,
                }
            ]
        }
    
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return preference