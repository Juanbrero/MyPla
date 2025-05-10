from sqlalchemy.orm import Session
from sqlalchemy import select, delete, insert
from app.models.RecurrentSchedule import RecurrentSchedule

from app.bd.schemas import schema_recurrent, schema_prof
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date
from app.bd.bd_utils import strip_time_hour_minute, valid_time, include_time
from app.bd.bd_exceptions import MinuteError, CompleteHour, WeekError

#Estas funciones no son utilizadas ya que se ingresa por TopicRecurrent

def get_all_recurrent(db: Session, recurrent:schema_prof.ProfessionalID):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.prof_id == recurrent.prof_id)
    response = db.scalars(smt).all()
    return response


def create_recurrent(db: Session, recurrent: schema_recurrent.RecurrentSchema):
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
        recurrent.end = strip_time_hour_minute(recurrent.end)
    except MinuteError as e:
        return {'error':f'{ e}'}
    
    try:
        if recurrent.week_day not in range(1, 8):
            raise WeekError(recurrent.week_day)
    except WeekError as e:
        return {'error':f'{ e}'}
    
    try:
        if valid_time(recurrent):
            existent = __get_schedule(db, recurrent)
            if not include_time(existent, recurrent):
                try:
                    stm = insert(RecurrentSchedule).values(recurrent.dict())
                    response = db.execute(stm)
                    db.commit()
                except:
                    return {'error':'on create_recurent'}
                return recurrent
            else:
                return {'error':'time include in DB'}
        else:
            return {'error': f'Same hour {recurrent.start} == {recurrent.end}'}
    except CompleteHour as e:
        return {'error':f'{ e}'}
    except:
        return {'error': 'invalid time'}
    
def get_day(db: Session, recurrent: schema_recurrent.RecurrentSchema):
    smt = select(RecurrentSchedule).where(RecurrentSchedule == recurrent)
    response = db.scalars(smt).all()
    return response

def del_day(db:Session, recurrent: schema_recurrent.RecurrentSchema): 
    recurrent.start = strip_time_hour_minute(recurrent.start)
    try:
        smt = delete(RecurrentSchedule).where(RecurrentSchedule == recurrent)
        db.execute(smt)
        db.commit()
    except:
        return {'error':'Not posible delete'}
    return recurrent


def __get_schedule(db: Session, recurrent:schema_recurrent.RecurrentSchema):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.prof_id == recurrent.prof_id,
                                           RecurrentSchedule.week_day == recurrent.week_day)
    response = db.scalars(smt).all()
    return response
