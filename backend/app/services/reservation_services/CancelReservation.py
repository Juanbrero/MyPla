from app.models import Reservation
from app.bd.repositories.Repository import Repository

from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime, timedelta

class CancelReservation():
    @handle_errors
    def run(
        db : Session,
        day_hour : datetime,
        user_id : str,
        user_cancel : str,
        role : str,
        reservationR : Repository[Reservation]
    ):
        day_hour = day_hour.replace(second=0, microsecond=0)

        reservation_filter ={
            'day_hour': day_hour,
            'prof_id': user_cancel if role == "Profesional" else user_id,
            'student_id': user_cancel if role == "Alumno" else user_id,
            'state': "pay"
        }

        reserva = reservationR.get_by(reservation_filter)
        
        if len(reserva) == 0:
            raise NotFound("Reservation to cancel not found")
        
        if reserva[0].day_hour - datetime.now() < timedelta(days=1):
            raise ValidationError("The reservation is less than one day ")

        if role == "Alumno":
            reservationR.update(filters=reservation_filter,
                                values={"cancel": True,
                                        "cancel_time": datetime.now(),
                                        "state": "cancel_student"
            })
        else:
            reservationR.update(filters=reservation_filter,
                                values={"cancel": True,
                                        "cancel_time": datetime.now(),
                                        "state": "cancel_professional"
            })
        
        db.commit()

        return JSONResponse(status_code= status.HTTP_202_ACCEPTED, content='Reservation canceled')