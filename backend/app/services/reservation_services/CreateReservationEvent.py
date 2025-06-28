from app.utils.errors import handle_errors, ValidationError, NotFound
from app.models import Reservation, Event, Meeting, ProfessionalTopic, Class, RecurrentSchedule, SpecificSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_reservation 
from datetime import timedelta, date
from app.bd.bd_utils import Schedule, valid_time
from fastapi.responses import JSONResponse
from fastapi import status

class CreateReservationEvent:
    @handle_errors
    def run (
        db: Session,
        reservationR: Repository[Reservation],
        eventR: Repository[Event],
        reservationS: schema_reservation.ReservationEvent,
        student_id: str
    ):
        reservationR.delPending()

        student_reserv = reservationR.get_by({'student_id': student_id, 
                                              "day_hour":reservationS.day_hour,
                                               "state":"pay"})
        
        if len(student_reserv) > 0:
            raise ValidationError("You have a reservation to this hour")
        
        reservation = reservationR.get_by({
            "student_id": student_id,
            "state": 'pending'
        })
        
        if (len(reservation) > 0):
            reservationR.delete({
                "student_id": student_id,
                "state": 'pending'
            })
        
        events = eventR.get_by({
            "day_hour": reservationS.day_hour,
            "prof_id": reservationS.prof_id
        })
        
        if len(events) <= 0:
            raise NotFound("Event doesn't exist")
        
        reservationsEvent = reservationR.get_by({
            "prof_id": reservationS.prof_id,
            "day_hour": reservationS.day_hour,
            "student_id": student_id
        })
        
        if len(reservationsEvent) > 0:
            raise ValidationError("You are already registered in the event")
        
        
        reservationR.create(
            {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "student_id": student_id
            }
        )
        
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Start event reservation")
        
        