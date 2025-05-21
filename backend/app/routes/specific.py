
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Annotated, Union

from app.bd.schemas import schema_topic_specific, schema_response
from app.repository.specific_repository import SpecificRepository
from app.bd.cruds import crud_topic_specific, crud_prof
from app.bd.bd_utils import Errors, Info
from datetime import date, time


router = APIRouter(prefix="/professionals/{prof_id}/agenda/specifics")

#SPECIFIC

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


@router.post('', tags=['Specific'])
def create_specific(prof_id:str, specific: schema_topic_specific.SpecificInsert, db: Session = Depends(get_db)):
    # Topicos
    # Validar Professional

    specific_repo = SpecificRepository(db)
    specific.start = specific_repo.trunc_time(specific.start)
    specific.end = specific_repo.trunc_time(specific.end)
    insert = schema_topic_specific.SpecificSchema(**specific.dict(), prof_id= prof_id)

    validateTime(insert,specific_repo)

    sele = schema_topic_specific.SpecificDaySID(**insert.dict())
    db_specific = specific_repo.get_day(sele)

    if not db_specific is None:
        raise HTTPException(status_code=400, detail='Dia especifico ya existente')
    
    response = specific_repo.create(insert)
    return response

@router.get('/day', tags=['Specific'])
def get_specific_day(prof_id: str, day:date, db:Session = Depends(get_db)):
    specific_repository = SpecificRepository(db)
    specific_get = schema_topic_specific.SpecificDayID(day= day, prof_id=prof_id)
    specific = specific_repository.get_day_hours(specific_get)
    return {'specific': specific}

@router.get('', tags=['Specific'])
def get_specific_month_year(prof_id: str, 
                            month: int,
                            year: int | None = None, 
                            db: Session = Depends(get_db)):
    specific_repository = SpecificRepository(db)
    if year is None:
        year = date.today().year
    if not month in range(0, 13):
        raise HTTPException(status_code=400, detail='Valor de mes invalido')
    specific = schema_topic_specific.TopicSpecificMonthYear(month= month, year= year, prof_id= prof_id)
    month_year = specific_repository.get_month_year(specific)
    return {'specific': month_year }

@router.put('', tags=['Specific'])
def update_specific(prof_id: str, specific_update:schema_topic_specific.SpecificUpdateInfo, db: Session= Depends(get_db)):
    
    if specific_update.Nstart is None and specific_update.Nend is None:
        raise HTTPException(status_code=400, detail='Not update')
    
    specific_repository = SpecificRepository(db)

    specific_update.start = specific_repository.trunc_time(specific_update.start)

    sele = schema_topic_specific.SpecificDaySID(**specific_update.dict(), prof_id= prof_id)
    db_specific = specific_repository.get_day(sele)

    if db_specific is None:
        raise HTTPException(status_code=404, detail='Day not found')
    
    update = schema_topic_specific.SpecificGet.from_orm(db_specific)
    
       
    if not specific_update.Nstart is None:
        update.start = specific_repository.trunc_time(specific_update.Nstart)
    if not specific_update.Nend is None:
        update.end =  specific_repository.trunc_time(specific_update.Nend)
   
    
    validateTime(update, specific_repository, sele.start)
    
    sucess = specific_repository.update(db_specific, update)
    return sucess


@router.delete('', tags=['Specific'])
def delete_specific(prof_id: str, day:date, start:time, db: Session = Depends(get_db)):
    specific_repository = SpecificRepository(db) 

    data = schema_topic_specific.SpecificDaySID(day=day, start= specific_repository.trunc_time(start), prof_id= prof_id)
    db_specific = specific_repository.get_day(data)
    if db_specific is None:
        raise HTTPException(status_code=404, detail='Day not found')
    sucess = specific_repository.delete(db_specific)
    return {'detail':'Day deleted sucessfully'}


##################################################
#Crea el dia disponible especifico, con los topicos
#@router.post('/specific/test',tags=["Specific"])
def create_specific_day(prof_id:str, specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia especifico
    """
    db_prof  = crud_prof.get_prof_id(db,prof_id= prof_id)
    if db_prof is None:
        raise HTTPException(status_code=404, detail='Professional not exist')
    
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= prof_id, isCanceling= False)
    sucess = crud_topic_specific.create_specific(db, topicS)
    if type(sucess) == dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return sucess
    

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
#@router.get('/specific',tags=["Specific"])
def get_specific(prof_id:str, day: date, hour: time,  db:Session = Depends(get_db)):
    """
    Recupercion de todos los dias especificos de un profesional
    """
    topicS = schema_topic_specific.TopicSpecificDel(day=day, start=hour, prof_id=prof_id)
    return crud_topic_specific.get_specific(db, topicS)


#@router.get('/specific/{month}', tags=['Specific'], response_model=Union[schema_response.ResponseSpecific,Errors] ,summary='Codigo que recupera todos los dias (Especificos) de un profesional en un mes determinado')
def get_specific_month(prof_id:str, month:int, db:Session = Depends(get_db)):
    """
    # On agenda

    ## Prueba de recuperación de los dias especificos dado un mes
    - month: int(1-12)
    - prof_id: str
    """
    if not month in range(0,13):
        raise HTTPException(status_code=400, detail='Valor de mes incorrecto')
    topic = schema_topic_specific.TopicSpecificMonth(prof_id=prof_id, month=month)
    return crud_topic_specific.get_id_month(db, topic)


#@router.put('/specific', tags=['Specific'])
def update_specific(prof_id:str, update:schema_topic_specific.SpecificUpdateInfo, db:Session = Depends(get_db)):
    spec = schema_topic_specific.TopicSpecificUpdate(**update.dict(), prof_id=prof_id)
    success = crud_topic_specific.update_specific(db, spec)
    if type(success) == dict:
        raise HTTPException(status_code=400, detail=success.get('error'))
    return {'detail':'Update sucessfully'}
        

#@router.delete('/specific', tags=['Specific'])
def del_specific(prof_id:str, spec:schema_topic_specific.SpecificDat, db: Session = Depends(get_db)):
    specific = schema_topic_specific.TopicSpecificDel(**spec.dict, prof_id=prof_id)
    sucess = crud_topic_specific.delete_specific(db, specific)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail': 'Deleted sucessfully'}


@router.post('/specific/topic/', tags=['Specific'], response_model=Union[schema_topic_specific.TopicSpecificCreate, Errors])
def add_specific_topic(prof_id:str, specific:schema_topic_specific.TopicSpecificBase, db:Session = Depends(get_db)):
    """
    Agrega un topico a un dia especifico particular
    """
    specific_topic = schema_topic_specific.TopicSpecificCreate(**specific.dict(), prof_id=prof_id)
    sucess = crud_topic_specific.add_topic_specific(db, specific_topic)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return sucess


@router.delete('/specific/topic/', tags=['Specific'])
def del_specific_topic(prof_id:str, specific:schema_topic_specific.TopicSpecificBase, db:Session = Depends(get_db)):
    """
    Elimina un topico de un dia especifico
    """
    specific_topic = schema_topic_specific.TopicSpecificCreate(**specific.dict(), prof_id= prof_id)
    sucess = crud_topic_specific.del_topic_specific(db, specific_topic)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail': 'Deleted Topic from Specific'}
    


