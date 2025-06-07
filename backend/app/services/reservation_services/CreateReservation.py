from app.utils.errors import handle_errors, ValidationError, NotFound
from app.models import Reservation, Meeting, ProfessionalTopic, Class, RecurrentSchedule, SpecificSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_reservation 
from datetime import timedelta
from app.bd.bd_utils import Schedule, valid_time
from fastapi.responses import JSONResponse
from fastapi import status

class CreateReservation ():
    @handle_errors
    def run (
        db: Session,
        reservationR: Repository[Reservation],
        meetingR: Repository[Meeting],
        professional_topicR: Repository[ProfessionalTopic],
        recurrentR: Repository[RecurrentSchedule],
        specificR: Repository[SpecificSchedule],
        classR: Repository[Class],
        reservationS: schema_reservation.ReservationClassIn
    ):
        
        reservationS.day_hour = reservationS.day_hour.replace(second=0, microsecond=0)
        day = reservationS.day_hour.date()
        start = reservationS.day_hour.time()
        end = (reservationS.day_hour + timedelta(hours=1)).time()
        topic = reservationS.topic

        schedule_class = Schedule(start=start, end=end)
        
        reservation = reservationR.get_by({
            "student_id": reservationS.student_id,
            "state": 'pending'
        })
        
        if (len(reservation) > 0):
            raise ValidationError("You have a pay pending")

        if start.minute != 0 and start.minute != 30 and valid_time(schedule_class):
            raise ValidationError('Format to hour is incorrect')
        
        exception= specificR.getExceptionToClass(reservationS.prof_id, reservationS.day_hour)

        if len(exception) > 0:
            raise NotFound("The professional is not available at the moment")
        
        specific= specificR.getSpecificToClass(reservationS.prof_id, reservationS.topic, reservationS.day_hour)

        if len(specific) <= 0:
            recurrent= recurrentR.getRecurrentToClass(reservationS.prof_id, reservationS.topic, reservationS.day_hour)
            print(recurrent)
            if len(recurrent) <= 0:
                raise NotFound("The professional does not have a schedule for this class")
        
        meetings = meetingR.get_by(
            {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "topic_name": reservationS.topic
            }
        )
        if not (meetings is None) and len(meetings) > 0:
            raise ValidationError("The professional has a meeting at that time")
        
        topic = professional_topicR.get_by(
            {
                "prof_id": reservationS.prof_id,
                "topic_name": reservationS.topic
            }
        )
        
        if topic is None or len(topic) == 0:
            raise ValueError("No price was found for that teacher and subject.")
        
        topic = topic[0]
        
        price_value = topic.price_class  # Obtener el valor del precio
        
        meetingR.create({
            "prof_id": reservationS.prof_id,
            "day_hour": reservationS.day_hour,
            "topic_name": reservationS.topic
        })
        
        db.flush()
        
        # 3. Creamos la clase
        classR.create(
            {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "price": price_value
            }
        )
        
        # 4. Creamos la reserva
        reservationR.create(
            {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "student_id": reservationS.student_id
            }
        )
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Start class reservation")
    
    #def insert_reservation_class (db: Session, reservationS: schema_reservation.ReservationClassIn):
        