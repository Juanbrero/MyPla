from app.bd.bd_utils import Errors, Info
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas import schema_response, schema_exception
from app.bd.schemas.schema_prof import ProfessionalID
from app.bd.cruds import crud_exception, crud_prof
from app.repository.exception_repository import ExceptionRepository
from datetime import date, time

from app.bd.schemas import schema_exception

router = APIRouter(prefix="/professionals/{prof_id}/agenda/exceptions")


#Exception

def validateTime(obj, respository, Ostart: time = None):
    """
        - obj
            - day/week
            - start
            - end
            - prof_id
    """
    if not respository.isCompleteHour(obj.start, obj.end):
        raise HTTPException(status_code=400, detail='No es una hora completa')
    if not respository.isValidTime(obj.start,obj.end):
        raise HTTPException(status_code=400, detail='Start > End incorrect')
    if Ostart is None:
        if respository.isInclude(obj):
            raise HTTPException(status_code=400, detail='Time include')
    else:
        if respository.isIncludeUpdate(Ostart, obj):
            raise HTTPException(status_code=400, detail='Time incluide')

@router.post('', tags=['Exception'], response_model= schema_exception.ExceptionGet)
def create_exception(prof_id:str, excep: schema_exception.ExceptionBase, db: Session = Depends(get_db)):
    exception_repository = ExceptionRepository(db)
    insert = schema_exception.ExceptionCreate(**excep.dict(), prof_id= prof_id)

    insert.start = exception_repository.trunc_time(insert.start)
    insert.end = exception_repository.trunc_time(insert.end)
    

    validateTime(insert, exception_repository)


    db_exception = exception_repository.get_day(insert)
    if not db_exception is None:
        raise HTTPException(status_code=400, detail='Recurrent day exist')
    
    return exception_repository.create(insert)
    
@router.get('/day', tags=['Exception'])   
def get_day(prof_id: str, day:date, db:Session = Depends(get_db)):
    exception_repository = ExceptionRepository(db)

    excep_get = schema_exception.ExceptionGetDat(day= day, prof_id= prof_id)
    response = exception_repository.get_day_hours(excep_get)

    return {'exception': response}


@router.get('', tags=['Exception'])
def get_month_year(prof_id: str, 
                            month: int,
                            year: int | None = None, 
                            db: Session = Depends(get_db)):
    exception_repository = ExceptionRepository(db)
    if year is None:
        year = date.today().year
    if not month in range(0, 13):
        raise HTTPException(status_code=400, detail='Valor de mes invalido')
    specific = schema_exception.ExceptionMonthYear(month= month, year= year, prof_id= prof_id)
    month_year = exception_repository.get_month_year(specific)
    return {'exception': month_year }
    
@router.put('', tags=['Exception'])
def update_exception(prof_id:str, exception_update: schema_exception.ExceptionUp, db:Session = Depends(get_db)):
    
    if exception_update.Nstart is None and exception_update.Nend is None:
        raise HTTPException(status_code=400, detail='Not update')
    
    exception_repository = ExceptionRepository(db)
    

    exception_update.start = exception_repository.trunc_time(exception_update.start)

    sele = schema_exception.ExceptionDel(**exception_update.dict(), prof_id= prof_id)
    db_exception = exception_repository.get_day(sele)

    if db_exception is None:
        raise HTTPException(status_code=404, detail='Day not found')
    
    update = schema_exception.ExceptionGet.from_orm(db_exception)
    
       
    if not exception_update.Nstart is None:
        update.start = exception_repository.trunc_time(exception_update.Nstart)
    if not exception_update.Nend is None:
        update.end =  exception_repository.trunc_time(exception_update.Nend)
   
    
    validateTime(update, exception_repository, sele.start)
    
    sucess = exception_repository.update(db_exception, update)
    return sucess


@router.delete('', tags=['Exception'])
def del_exception(prof_id:str, day: date, start:time, db: Session = Depends(get_db)):
    exception_repository = ExceptionRepository(db)
    excep_del = schema_exception.ExceptionDel(start= exception_repository.trunc_time(start), day= day, prof_id= prof_id)

    db_exception = exception_repository.get_day(excep_del)
    if db_exception is None:
        raise HTTPException(status_code=404, detail='Day not found')
    sucess = exception_repository.delete(db_exception)
    return {'detail':'Day deleted sucessfully'}


#############################################
#crear excepciones, iscanceling= True
#@router.post('/exceptions', tags=["Exception"], response_model=schema_exception.ExceptionGet)
def create_exception(prof_id:str, excep:schema_exception.ExceptionBase, db: Session = Depends(get_db)):
    """
    Creacion de una excepcion
    """
    db_professional = crud_prof.get_prof_id(db, prof_id)
    if db_professional is None:
        raise HTTPException(status_code=404, detail='Professional not exist')
    excepcion = schema_exception.ExceptionCreate(**excep.dict(), prof_id= prof_id)
    exception = crud_exception.create_exception(db, excepcion)
    if type(exception) is dict:
        raise HTTPException(status_code=400, detail=exception.get('error'))
    return exception

#@router.get('/exceptions', tags=["Exception"], response_model=schema_response.ResponseException)
def get_exception(prof_id:str, month:int, db: Session = Depends(get_db)):
    """
    Funcion que por el momento, ignora el dia, el objetivo sera utilizarlo
    - prof_id:str
    """
    if month in range(1,13):
        raise HTTPException(status_code=400, detail='Value Month invalid')
    
    excepcion = schema_exception.ExceptionMonth(prof_id= prof_id, month= month)
    return crud_exception.get_exception(db, excepcion)

#@router.put('/exceptions', tags=['Exception'])
def update_exception(prof_id:str, excep:schema_exception.ExceptionUp, db:Session = Depends(get_db)):
    """
    Permite actualizar la hora de inicio y/o hora de final dado una hora de inicio

    Args:
       - prof_id: str
       - day: int
       - start: time <- Hora a actualizar 
       - Nstart: time | None
       - Nend: time | None
    """
    excepU = schema_exception.ExceptionUpdate(**excep.dict(), prof_id= prof_id)
    sucess = crud_exception.update_exception(db, excepU)
    if type(sucess):
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail': 'Correct update'}



#@router.delete('/exceptions', tags=['Exception'])
def del_exception(prof_id:str, excep:schema_exception.ExceptionDelDat, db:Session = Depends(get_db)):
    """
    Eliminación de una excepcion
    """
    excepD = schema_exception.ExceptionDel(**excep.dict(), prof_id=prof_id)
    sucess = crud_exception.delete_exception(db, excepD)
    if type(sucess) is dict:
        raise HTTPException(status_code=404, detail='Exception not found')
    return {"detail": "Exception deleted successfully"}



