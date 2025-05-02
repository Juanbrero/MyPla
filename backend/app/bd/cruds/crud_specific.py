from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert
from app.models.SpecificSchedule import SpecificSchedule
from app.bd.schemas import schema_specific
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date, time

from app.bd.bd_utils import strip_time_hour_minute, valid_time, include_time
from app.bd.bd_exceptions import MinuteError, CompleteHour

def get_exception(db: Session, excepcion: schema_specific.SpecificID):
    try:
        smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == excepcion.prof_id, SpecificSchedule.isCanceling == True)
        response = db.scalars(smt).all()
        respuesta = [schema_specific.Specific(day=r.day, start=r.start, end=r.end) for r in response]
        return respuesta
    except:
        return {'error': 'No fue posible recuperar'}


def create_exception(db: Session, spec: schema_specific.SpecificIsCancel):
    try:
        spec.start = strip_time_hour_minute(spec.start) #10:20:06.25..z -> 10:20
        spec.end= strip_time_hour_minute(spec.end)
    except MinuteError as e:
        return {'error':f'{e}'}
    try:
        if valid_time(spec):
            existent = __get_schedule(db, spec)
            if not include_time(db, spec):
                try:
                    smt = insert(SpecificSchedule).values(spec.dict())
                    response = db.execute(smt)
                    db.commit()
                except:
                    return {'error':'on create_spec'}
                return spec
            else:
                return {'error':'time include'}
        else:
            return {'error': f'Same hour {spec.start} == {spec.end}'}
    except CompleteHour as e:
        return {'error': f'{e}'}
    except:
        return {'error':'invalid time'}

def __get_schedule(db: Session, spec:schema_specific.SpecificSchema):
    smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == spec.prof_id).where(SpecificSchedule.day == spec.day)
    response = db.scalars(smt).all()
    return response


#Codigo antigua para especifico
def get_day(db:Session, spec:schema_specific.SpecificSchema):
    return  db.query(SpecificSchedule).filter(SpecificSchedule.prof_id == spec.prof_id).all()


def del_day(db:Session, spec: schema_specific.SpecificSchema): 
    spec.start = strip_time_hour_minute(spec.start)
    try:
        smt = delete(SpecificSchedule).where(SpecificSchedule.start == spec.start,
                                              SpecificSchedule.day == spec.day,
                                              SpecificSchedule.prof_id == spec.prof_id)
        db.execute(smt)
        db.commit()
    except:
        return {'error':'Not posible delete'}
    return spec



