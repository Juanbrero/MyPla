from sqlalchemy.orm import Session
from app.models import Reservation, Meeting, Class, Cancelation
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
        reservationS: schema_reservation.PayPending,
        cancelationR: Repository[Cancelation]
    ):
        reservations = reservationR.getReservationForTransaction({
            "day_hour": reservationS.day_hour,
            "prof_id": reservationS.prof_id,
            "student_id": reservationS.student_id
        })
        
        cancelations = cancelationR.get_by({
            "prof_id": reservationS.prof_id,
            "day_hour": reservationS.day_hour,
            "student_id": reservationS.student_id,
            "refund": False
        })

        if len(reservations) <= 0 and len(cancelations) <= 0:
            raise NotFound('Not pay pendig')
        
        if len(reservations) > 0:
            r = reservations[0]
            
            print('finished')
            reservationR.update({
                "state": 'finished'
            }, {
                "day_hour": r.day_hour,
                "prof_id": r.prof_id,
                "student_id": r.student_id
            })
        else:
            c = cancelations[0]
            
            print("refund")
            cancelationR.update({
                "refund": True
            }, {
                "prof_id": c.prof_id,
                "student_id": c.student_id,
                "day_hour": c.day_hour
            })


        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content='Pay modify')