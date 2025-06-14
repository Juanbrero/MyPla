from app.utils.errors import handle_errors, ValidationError, NotFound
from app.models import Reservation
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_reservation 
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from fastapi import status

class StudentReservation:
    @handle_errors
    def run(
        student_id: str,
        reservationR: Repository[Reservation]
    ):
        
        class_ = reservationR.getStudent(student_id)
        reservas = []
        for reserva, topic, username, link in class_:
            item = {
                "prof_username": username,
                "prof_id": reserva.prof_id,
                "day_hour": reserva.day_hour.isoformat(),
                "topic": topic,
                "link_class": link
            }
            reservas.append(item)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"reservations": reservas})