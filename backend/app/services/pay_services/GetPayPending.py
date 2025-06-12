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


class GetPayPending:
    @handle_errors
    def run (
        reservationR: Repository[Reservation]
    ):
        reservations = reservationR.getReservationsForTransaction()
        response = []
        for reservation, professional, student, prof_email, stud_email ,price in reservations:
            print(stud_email)
            rData = {
                "type": 'pay' if reservation.state == 'pay' else 'refund',
                "price": price,
                "cvu": professional.cvu if reservation.state == 'pay' else student.cvu,
                "day_hour": reservation.day_hour.isoformat(),
                "user_student": {
                    "student_id": student.student_id,
                    "email": stud_email
                },
                "user_professional": {
                    "professional_id": professional.prof_id,
                    "email": prof_email
                }
            }
            
            if reservation.state != 'pay':
                rData["day_hour_cancel"] = reservation.cancel_time.isoformat()
            response.append(rData)
        
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)