from sqlalchemy.orm import Session
from app.models.Reservation import Reservation
from app.models.Class import Class
from app.models.Meeting import Meeting
from app.models.Professional import Professional
from app.models.ProfessionalTopic import ProfessionalTopic
from datetime import timedelta, datetime
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from app.bd.schemas import schema_reservation 
from sqlalchemy import select, exc
from ..bd_utils import error_hand, Schedule, include_time, include_time1, valid_time
import traceback

from app.bd.schemas import schema_prof
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific

def create_reservation_class(db:Session, reservationS:schema_reservation.ReservationClassIn):
    """
    Crea una reserva a una clase y crea la reunion
    
    Args:
        db (Session): Database conection
        reservation (schema_reservation.ReservationClassIn)
            - day_hour: daytime
            - prof_id: str
            - topic: str
            - student_id: str
    Returns:
        { 'message': 'Reserva creada con exito'}
        {'error':}
    """

    try:
        day = reservationS.day_hour.date()
        start = reservationS.day_hour.time()
        end = (reservationS.day_hour + timedelta(hours=1)).time()
        topic = reservationS.topic
        week_day = reservationS.day_hour.isoweekday()

        schedule_class = Schedule(start=start, end=end)

        if start.minute != 0 and start.minute != 30 and valid_time(schedule_class):
            return {'message': 'El horario tiene un formato incorrecto'}
        
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
            print(recurrent, week_day)
            recurrent_day = None
            while i < len(recurrent) and recurrent_day is None:
                r = recurrent[i]
                print(r.start, schedule_class.start, r.end, schedule_class.end, week_day, r.week_day, r.week_day == week_day and r.start <= schedule_class.start and r.end >= schedule_class.end)
                if r.week_day == week_day and r.start <= schedule_class.start and r.end >= schedule_class.end:
                    recurrent_day = r
                i += 1
            if not (recurrent_day is None) and {"topic_name": topic} in recurrent_day.topics:
                valid = True
        
        if not valid:
            return {'error': 'El profesor no esta disponible en ese horario'}
        
        insert_reservation_class(db, reservationS)
        return {'message': 'Se genero la reserva y la clase'}
    except Exception as e:
        print(e)
        return {'error': 'Error al generar la nueva clase'}

def insert_reservation_class (db: Session, reservationS: schema_reservation.ReservationClassIn):
    meeting = Meeting(
        prof_id=reservationS.prof_id,
        day_hour=reservationS.day_hour,
        topic_name=reservationS.topic
    )
    db.add(meeting)
    db.commit()

    # 2. Consultamos el precio
    topic = db.query(ProfessionalTopic.price_class).filter(
        (ProfessionalTopic.prof_id == reservationS.prof_id) &
        (ProfessionalTopic.topic_name == reservationS.topic)
    ).first()
    
    if topic is None:
        raise ValueError("No se encontró el precio para ese profesor y tema.")
    
    price_value = topic.price_class  # Obtener el valor del precio
    
    # 3. Creamos la clase
    class_ = Class(
        prof_id=reservationS.prof_id,
        day_hour=reservationS.day_hour,
        price=price_value
    )
    
    db.add(class_)
    
    # 4. Creamos la reserva
    reservation = Reservation(
        prof_id=reservationS.prof_id,
        day_hour=reservationS.day_hour,
        student_id=reservationS.student_id
    )
    
    db.add(reservation)
    db.commit()
    #meeting = Meeting(prof_id=reservationS.prof_id, day_hour=reservationS.day_hour, topic_name=reservationS.topic)
#
    #db.add(meeting)
    #price = db.query(ProfessionalTopic.price_class).filter((ProfessionalTopic.prof_id == reservationS.prof_id) & (ProfessionalTopic.topic_name == reservationS.topic)).first()
    #
    #class_ = Class(prof_id=reservationS.prof_id, day_hour=reservationS.day_hour, price=price)
    #db.add(class_)
    #
    #reservation = Reservation(prof_id=reservationS.prof_id, day_hour=reservationS.day_hour, student_id=reservationS.student_id)
    #db.add(reservation)
    #db.commit()