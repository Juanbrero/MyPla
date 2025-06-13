from sqlalchemy.orm import Session
from app.models import Reservation, Meeting, Class
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_reservation
from datetime import datetime, timedelta
# SDK de Mercado Pago
from os import getenv
import mercadopago
# Agrega credenciales (private key)
sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))


class ModifyPayPending:
    @handle_errors
    def run (
        db: Session,
        reservationR: Repository[Reservation],
        reservationS: schema_reservation.PayPending
    ):
        reservations = reservationR.getReservationForTransaction({
            "day_hour": reservationS.day_hour,
            "prof_id": reservationS.prof_id,
            "student_id": reservationS.student_id
        })
        
        if len(reservations) <= 0:
            raise NotFound('Reservation not exist')
        
        r = reservations[0]
        
        print('finished' if r.state == 'pay' else 'refund')
        reservationR.update({
            "state": 'finished' if r.state == 'pay' else 'refund' 
        }, {
            "day_hour": r.day_hour,
            "prof_id": r.prof_id,
            "student_id": r.student_id
        })
        
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content='Pay modify')