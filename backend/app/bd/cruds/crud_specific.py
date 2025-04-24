from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.SpecificSchedule import SpecificSchedule
from app.bd.schemas import schema_specific
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date, time

from app.bd.bd_utils import strip_time_hour_minute, valid_time, incluide_time, MinuteError


def get_all_specific(db: Session):
    return db.query(SpecificSchedule).all()


def create_specific(db: Session, spec: schema_specific.SpecificCreate, id_prof:int):
    spec.start = strip_time_hour_minute(spec.start) #10:20:06.25..z -> 10:20
    spec.end= strip_time_hour_minute(spec.end)
    try:
        if valid_time(spec.start, spec.end):
            existent = __get_schedule(db, id_prof, spec.day)
            if not incluide_time(db, spec.start, spec.end):
                try:
                    db_spec = SpecificSchedule(**spec.dict(), user_id=id_prof)
                    db.add(db_spec)
                    db.commit()
                    db.refresh(db_spec)
                except:
                    db_spec = {'error':'on create_spec'}
                return db_spec
            else:
                return {'error':'time include'}
        else:
            return {'error':'invalid time'}
    except MinuteError:
        return {'error': 'Minute Accept 00 or 30'}

def iscaceled_specific(db:Session, day_in:date, id_prof:int, hour:time) -> schema_specific.SpecificIsCancel:
    hour = strip_time_hour_minute(hour)
    smt = select(SpecificSchedule).where( SpecificSchedule.day == day_in, 
                                             SpecificSchedule.user_id == id_prof,
                                             SpecificSchedule.start == hour)
    response = db.scalars(smt).all()
    return response

def cancel_day(db:Session, prof_id:int, day:date, hour:time):
    hour = strip_time_hour_minute(hour)
    db.query(SpecificSchedule).filter(SpecificSchedule.day == day, 
                                      SpecificSchedule.start == hour, 
                                      SpecificSchedule.user_id == prof_id).update({"isCanceling":True})
    db.commit()
    return db.query(SpecificSchedule).all()

def get_day(db:Session, prof_id:int):
    return  db.query(SpecificSchedule).filter(SpecificSchedule.user_id == prof_id).all()


def __get_schedule(db: Session, id_prof:int, day:time):
    smt = select(SpecificSchedule).where(SpecificSchedule.user_id == id_prof).where(SpecificSchedule.day == day)
    response = db.scalars(smt).all()
    return response

