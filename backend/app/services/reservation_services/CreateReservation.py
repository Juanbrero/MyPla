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

        if start.day != end.day:
            raise ValidationError('Change of day')

        schedule_class = Schedule(start=start, end=end)

        if start.minute != 0 and start.minute != 30 and valid_time(schedule_class):
            raise ValidationError('el horario no tiene un formato correcto')
        
        exception= specificR.getExceptionToClass(reservationS.prof_id, reservationS.day_hour)

        if len(exception) > 0:
            raise NotFound("El profesional no esta disponible en ese momento")
        
        specific= specificR.getSpecificToClass(reservationS.prof_id, reservationS.topic, reservationS.day_hour)

        if len(specific) <= 0:
            recurrent= recurrentR.getRecurrentToClass(reservationS.prof_id, reservationS.topic, reservationS.day_hour)
            if len(recurrent) <= 0:
                raise NotFound("El profesional no tiene horario para esa clase")
        
        meetings = meetingR.get_by(
            {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "topic_name": reservationS.topic
            }
        )
        if not (meetings is None) and len(meetings) > 0:
            raise ValidationError("El profesional tiene una reunion en ese momento")
        
        topic = professional_topicR.get_by(
            {
                "prof_id": reservationS.prof_id,
                "topic_name": reservationS.topic
            }
        )
        
        if topic is None or len(topic) == 0:
            raise ValueError("No se encontró el precio para ese profesor y tema.")
        
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Clase creada")
    
    #def insert_reservation_class (db: Session, reservationS: schema_reservation.ReservationClassIn):
        