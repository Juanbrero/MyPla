from sqlalchemy.orm import Session
from app.models import Reservation, Meeting, Class
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic
from datetime import datetime
from app.config.expire import EXPIRE_RESERVATION
# SDK de Mercado Pago
from os import getenv
import mercadopago
# Agrega credenciales (private key)
sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))


class CreatePreference:
    @handle_errors
    def run (
        reservationR: Repository[Reservation],
        classR: Repository[Class],
        student_id: str
    ):
        reservationR.delPending()

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

        preference_data = {
            "items": [
                {
                    "title": "Pago de reserva en MIPLA",
                    "quantity": 1,
                    "unit_price": c.price,
                }
            ],
            "date_of_expiration": (r.create + EXPIRE_RESERVATION).isoformat(),
            "metadata":{"student_id": student_id},
            "notification_url": "https://miplasip.publicvm.com/api/mp-notification?source_news=webhooks",
            "back_urls":{
                "success": "https://miplasip.publicvm.com/calendar",
                "failure": "https://miplasip.publicvm.com/profile"
            }
        }
   
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
       
        return preference