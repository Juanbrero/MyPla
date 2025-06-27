from app.models import Reservation, Cancelation, Meeting, Class
from app.bd.repositories.Repository import Repository

from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime
from app.config.expire import EXPIRE_DAY

class CancelReservation():
    @handle_errors
    def run(
        db : Session,
        day_hour : datetime,
        user_id : str,
        user_cancel : str,
        role : str,
        reservationR : Repository[Reservation],
        meetingR: Repository[Meeting],
        cancelationR: Repository[Cancelation],
        classR : Repository[Class]
    ):
        reservationR.delPending()

        day_hour = day_hour.replace(second=0, microsecond=0)

        reservation_filter ={
            'day_hour': day_hour.isoformat(),
            'prof_id': user_cancel if role == "Profesional" else user_id,
            'student_id': user_cancel if role == "Alumno" else user_id,
            'state': "pay"
        }

        reserva = reservationR.get_by(reservation_filter)
        
        if len(reserva) == 0:
            raise NotFound("Reservation to cancel not found")
        
        reserva = reserva[0]

        if reserva.day_hour - datetime.now() < EXPIRE_DAY:
            raise ValidationError("The reservation is less than one day ")
        
        clase = classR.get_by({'prof_id':reserva.prof_id, "day_hour": reserva.day_hour})
        cancel = cancelationR.get_by({"prof_id": reserva.prof_id, "student_id":reserva.student_id, "day_hour": reserva.day_hour})
        
        if len(cancel) != 0:
            raise ValidationError("This class was previously cancelled")


        if role == "Alumno":
            cancelationR.create({
                "prof_id": reserva.prof_id,
                "student_id": reserva.student_id,
                "day_hour": reserva.day_hour,
                "cancel_time": datetime.now(),
                "state": "cancel_student",
                "price": clase[0].price
            })

            meetingR.delete({'prof_id':reserva.prof_id,
                             'day_hour':reserva.day_hour})
            
            
        else:
            cancelationR.create({
                "prof_id": reserva.prof_id,
                "student_id": reserva.student_id,
                "day_hour": reserva.day_hour,
                "cancel_time": datetime.now(),
                "state": "cancel_professional",
                "price": clase[0].price
            })

            meetingR.delete({'prof_id':reserva.prof_id,
                             'day_hour':reserva.day_hour})
            
        db.commit()

        return JSONResponse(status_code= status.HTTP_202_ACCEPTED, content='Reservation canceled')