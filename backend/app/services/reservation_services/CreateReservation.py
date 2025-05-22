from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import Reservation, Meeting, ProfessionalTopic, Class
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_reservation 
from datetime import timedelta, datetime
from app.bd.bd_utils import error_hand, Schedule, include_time, include_time1, valid_time
from app.bd.schemas import schema_prof
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from fastapi.responses import JSONResponse
from fastapi import status

class CreateReservation ():
    @handle_errors
    def run (
        db: Session,
        reservationR: Repository[Reservation],
        meetingR: Repository[Meeting],
        professional_topicR: Repository[ProfessionalTopic],
        classR: Repository[Class],
        reservationS: schema_reservation.ReservationClassIn
    ):
        day = reservationS.day_hour.date()
        start = reservationS.day_hour.time()
        end = (reservationS.day_hour + timedelta(hours=1)).time()
        topic = reservationS.topic
        week_day = reservationS.day_hour.isoweekday()

        schedule_class = Schedule(start=start, end=end)

        if start.minute != 0 and start.minute != 30 and valid_time(schedule_class):
            raise ValidationError('el horario no tiene un formato correcto')
        
        prof = schema_prof.ProfessionalID(prof_id= reservationS.prof_id )
        recurrent= crud_topic_recurrent.get_recurrent(prof, db).get('recurrent')
        specific= crud_topic_specific.get_specific(prof, db).get('specific')
        exception= None#crud_specific.get_exception(db, prof).get('exception')

        if not (exception is None):
            for e in exception:
                if e.day == day and include_time(list(e), schedule_class):
                    return {'error': 'El profesor no esta disponible en ese horario'}
            
                
        specific_day = None
        if not (specific is None):
            i = 0
            s = None
            while i < len(specific) and specific_day is None:
                s = specific[i]
                if s.day == day and include_time(list(s), schedule_class):
                    specific_day = s
                i += 1
                
        valid = False

        if not (specific_day is None) and topic in specific_day.topics:
            valid = True
        
        if not valid:
            i = 0
            r = None
            recurrent_day = None
            while i < len(recurrent) and recurrent_day is None:
                r = recurrent[i]
                if r.week_day == week_day and r.start <= schedule_class.start and r.end >= schedule_class.end:
                    recurrent_day = r
                i += 1
            if not (recurrent_day is None) and {"topic_name": topic} in recurrent_day.topics:
                valid = True
        
        if not valid:
            raise NotFound("El profesor no esta disponible en ese horario")
        
        print(reservationS)
        try:
            data = {
                "prof_id": reservationS.prof_id,
                "day_hour": reservationS.day_hour,
                "topic_name": reservationS.topic
            }
            meeting = meetingR.create(**data)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error al insertar meeting: {e}")
            
        #meeting = meetingR.create(  
        #    {
        #        "prof_id": reservationS.prof_id,
        #        "day_hour": reservationS.day_hour,
        #        "topic_name": reservationS.topic
        #    }
        #)
        #db.commit()
    
        # 2. Consultamos el precio
        #topic = db.query(ProfessionalTopic.price_class).filter(
        #    (ProfessionalTopic.prof_id == reservationS.prof_id) &
        #    (ProfessionalTopic.topic_name == reservationS.topic)
        #).first()
        
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
        