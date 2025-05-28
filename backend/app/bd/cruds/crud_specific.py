from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert
from app.models.SpecificSchedule import SpecificSchedule
from app.bd.schemas import schema_specific
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date, time

from app.bd.bd_utils import strip_time_hour_minute, valid_time, include_time
from app.bd.bd_exceptions import MinuteError, CompleteHour

def create_exception(db: Session, spec: schema_specific.ExceptionCreate):
    """
    Crear  una excepcion, specific isCanceling= True

    Args:
        db: Session
        exception: schema_specific.ExceptionCreate
            - prof_id: str
            - day: date 
            - start: time 
            - end: time
    Return:
        {day:, start:, end:}
        {'error':}
    """
    excep = schema_specific.ExceptionInsert(**spec.dict())
    try:
        excep.start = strip_time_hour_minute(excep.start) #10:20:06.25..z -> 10:20
        excep.end= strip_time_hour_minute(excep.end)
    except MinuteError as e:
        return {'error':f'{e}'}
    try:
        if valid_time(spec):      
            existent = __get_schedule(db, spec)
            if not include_time(existent, spec):
                try:
                    smt = insert(SpecificSchedule).values(excep.dict())
                    response = db.execute(smt)
                    db.commit()
                except:
                    return {'error':'on create_exception'}
                return excep
            else:
                return {'error':'time include'}
        else:
            return {'error': f'Same hour {excep.start} == {excep.end}'}
    except CompleteHour as e:
        return {'error': f'{e}'}
    except:
        return {'error':'invalid time'}
    


def get_exception(db: Session, excepcion: schema_specific.ExceptionCreate):
    """
    Recuperar todas las excepciones

    Args:
        db: Session
        exception: schema_specific.ExceptionCreate
            - prof_id: str
            - day: date <- no considerado por ahora
            - start: time <- no considerado
            - end: time <- no considerado
    Return:
        {'exception':[schema_specific.ExceptionGet]}
            -   [{day:, start:, end:}]
        {'error':}
    """
    try:
        smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == excepcion.prof_id,
                                              SpecificSchedule.isCanceling == True)
        response = db.scalars(smt).all()
        respuesta = [schema_specific.ExceptionGet(day=r.day,
                                                   start=r.start, 
                                                   end=r.end) for r in response]
        return {'exception':respuesta}
    except:
        return {'error': 'No fue posible recuperar'}



def delete_exception(db:Session, excep:schema_specific.ExceptionDel):
    """
    Elimina una excepcion dado un dia, profesional y hora de inicio
    Args:
        db: Session
        excep: schema_specific.ExceptionDel
            - prof_id: str
            - day: date
            - start:time
    Return:
        {'info':}
        {'error':}    
    """
    excep.start = strip_time_hour_minute(excep.start)
    response = db.query(SpecificSchedule).filter(SpecificSchedule.isCanceling == True, 
                                                 SpecificSchedule.day == excep.day, 
                                                  SpecificSchedule.start == excep.start,
                                                   SpecificSchedule.prof_id == excep.prof_id ).first()
    if response is None:
        return {'error': f'not exist information'}
    db.delete(response)
    db.commit()
    return {'info':f'Delete -> Day: {excep.day}, start: {excep.start} from Professional: {excep.prof_id}'}


def update_exception(db:Session, exception:schema_specific.ExceptionUpdate):
    """
    Args:
        - db: Session
        - exception: schema_specific.ExceptionUpdate
            - prof_id: str
            - day: date
            - start: time
            - Nstart: time | None
            - Nend: time | None
    Return:
        - {'info': 'OK'}
        - {'error':}
    """
    try:
        exception.start = strip_time_hour_minute(exception.start)
    except MinuteError as  e:
        return {'error': f'{e}'}
    response = db.query(SpecificSchedule).where(SpecificSchedule.isCanceling == True,
                                                SpecificSchedule.day == exception.day,
                                                SpecificSchedule.prof_id == exception.prof_id,
                                                SpecificSchedule.start == exception.start).first()
    if response is None:
        return {'error': 'Exception not exist'}
    try:
        if not exception.Nend is None:
            response.end = strip_time_hour_minute(exception.Nend)
        if not exception.Nstart is None:
            response.start = strip_time_hour_minute(exception.Nstart)
    except MinuteError as e:
        return {'error':f'{e}'}
    if valid_time(response):
        exist = db.query(SpecificSchedule).where(SpecificSchedule.isCanceling == True,
                                                SpecificSchedule.day == exception.day,
                                                SpecificSchedule.prof_id == exception.prof_id,
                                                SpecificSchedule.start != exception.start).all()
        if not include_time(exist, response):
            try:
                updates = {'start': response.start, 'end':response.end}
                ic(updates)
                stm = update(SpecificSchedule).where(SpecificSchedule.isCanceling == True,
                                                    SpecificSchedule.day == exception.day,
                                                    SpecificSchedule.prof_id == exception.prof_id,
                                                    SpecificSchedule.start == exception.start).values(updates)
                db.execute(stm)
                db.commit()
                return {'info': 'OK'}
            except:
                return {'error':'On update Exception'}
        else:
            return {'error': 'time include in DB'}
    else:
        return {'error': f'Error hour {response.start} == {response.end}'} 
    

def __get_schedule(db: Session, spec:schema_specific.ExceptionGetDat):
    """
    Funcion privada que recupera todas las excepciones

    Args:
        db: Session
        spec: schema_specific.ExceptionGetDat
            - prof_id: str
            - day: date
    Return
        [SpecificSchedule]
        []

    """
    smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == spec.prof_id, 
                                         SpecificSchedule.day == spec.day, 
                                         SpecificSchedule.isCanceling == True)
    response = db.scalars(smt).all()
    return response
    