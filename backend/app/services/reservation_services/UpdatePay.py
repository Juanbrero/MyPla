from app.utils.errors import handle_errors, ValidationError, NotFound
from app.models import Reservation, Meeting

from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_reservation 
from datetime import timedelta, datetime

from fastapi.responses import JSONResponse
from fastapi import status


class UpdatePay():
    @handle_errors
    def run(
        db: Session,
        student_id: str,
        statusP: str, 
        reservationR: Repository[Reservation],
        meetingR: Repository[Meeting]
    ):
        """
        Ver estado del pago
        Ver vencimiento de reserva
        """
        reservations = reservationR.get_by({"student_id": student_id,
                                           "state": "pending"})
        if len(reservations) <= 0:
            raise NotFound("User not have a pending pay")
        
        r = reservations[0]


        if statusP == "cancelled":
            reservationR.delete({
                "student_id": student_id,
                "day_hour": r.day_hour.isoformat(),
                "state": "pending"
            })
            meetingR.delete({
                "prof_id": r.prof_id,
                "day_hour": r.day_hour.isoformat(),
            })

        if statusP == "rejected" and datetime.now() - r.create > timedelta(minutes= 3):
            reservationR.delete({
                "student_id": student_id,
                "day_hour": r.day_hour.isoformat(),
                "state": "pending"
            })
            meetingR.delete({
                "prof_id": r.prof_id,
                "day_hour": r.day_hour.isoformat(),
            })

        if statusP == "approved":
            
            reservationR.update({"state": "finished"}, {"student_id": student_id, "day_hour": r.day_hour.isoformat(), "state": "pending"})


        db.commit()

        return JSONResponse(status_code= status.HTTP_200_OK, content= 'Reservation update')
        
        

