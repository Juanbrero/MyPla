from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time

from app.bd.schemas import schema_topic_recurrent, schema_response, schema_recurrent
from app.bd.schemas.schema_prof import ProfessionalID
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_prof
from app.bd.bd_utils import Errors, Info
from app.bd.cruds import crud_exception
from app.repository.recurrent_repository import RecurrentRepository

router = APIRouter(prefix="/professionals/{prof_id}/agenda/recurrents")


#RECURRENT
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


@router.post('', tags=['Recurrent'])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.RecurrentCreate, db: Session = Depends(get_db)):
    # Topicos
    # Validar Professional
    recurrent_repository = RecurrentRepository(db)
    if not recurrent.week_day in range(0, 8):
        raise HTTPException(status_code=400, detail='Week Day incorrect')
    
    insert = schema_topic_recurrent.RecurrentSchema(**recurrent.dict(), prof_id= prof_id)
    insert.start = recurrent_repository.trunc_time(insert.start)
    insert.end = recurrent_repository.trunc_time(insert.end)
    validateTime(insert, recurrent_repository)

    db_recurrent = recurrent_repository.get_recurrent_week_start(insert)
    if not db_recurrent is None:
        raise HTTPException(status_code=400, detail='Day exist')
    response = recurrent_repository.create(insert)

    return response

@router.get('', tags=['Recurrent'])
def get_all(prof_id:str, db:Session = Depends(get_db)):
    recurrent_repository = RecurrentRepository(db)
    prof_id_get = schema_topic_recurrent.ProfessionalID(prof_id= prof_id)
    return recurrent_repository.get_recurrent(prof_id_get)

@router.get('/{week_day}', tags=['Recurrent'])
def get_week(prof_id:str, week_day:int, db:Session = Depends(get_db)):
    recurrent_repository = RecurrentRepository(db)
    if not week_day in range(0,8):
        raise HTTPException(status_code=400, detail='Week value invalid')
    week_get = schema_topic_recurrent.RecurrentWID(week_day= week_day,prof_id= prof_id)
    return recurrent_repository.get_recurrent_week(week_get)

@router.put('', tags=['Recurrent'])
def update_recurrent(prof_id:str, recurrent_update: schema_topic_recurrent.TopicRecurrentUp, db: Session = Depends(get_db)):
    
    if not recurrent_update.week_day in range(0, 8):
        raise HTTPException(status_code=400, detail='Week value invalid')
    
    if recurrent_update.Nstart is None and recurrent_update.Nend is None:
        raise HTTPException(status_code=400, detail='Not update')
    
    recurrent_repository = RecurrentRepository(db)
    sele = schema_topic_recurrent.RecurrentGet(week_day= recurrent_update.week_day, 
                                            start= recurrent_repository.trunc_time(recurrent_update.start), 
                                            prof_id= prof_id)
    
    db_selec = recurrent_repository.get_recurrent_week_start(sele)
    if db_selec is None:
        raise HTTPException(status_code=404, detail='Day not found')
    
    update = schema_topic_recurrent.RecurrentSchema.from_orm(db_selec)
    
    if not recurrent_update.Nstart is None:
        update.start = recurrent_repository.trunc_time(recurrent_update.Nstart)
    if not recurrent_update.Nend is None:
        update.end =  recurrent_repository.trunc_time(recurrent_update.Nend)

    validateTime( update, recurrent_repository, sele.start)
    sucess = recurrent_repository.update(db_selec, update)
    return sucess

@router.delete('', tags=['Recurrent'])
def del_recurrent(prof_id:str, week_day:int, start: time, db: Session = Depends(get_db)):
    if not week_day in range(0, 8):
        raise HTTPException(status_code=400, detail='Week value invalid')
    recurrent_repository= RecurrentRepository(db)
    
    sele = schema_topic_recurrent.RecurrentGet(week_day= week_day, 
                                               start= recurrent_repository.trunc_time(start), 
                                               prof_id= prof_id)
    db_recurrent = recurrent_repository.get_recurrent_week_start(sele)
    if db_recurrent is None:
        raise HTTPException(status_code=404, detail='Day not found')
    sucess = recurrent_repository.delete(db_recurrent)
    return {'detail': 'Day deleted sucessfully'}
    

##########################
#Crea el recurrent, con los topicos
#@router.post('/recurrent',tags=["Recurrent"], response_model=Union[schema_topic_recurrent.TopicRecurrentIn, Errors])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    if not recurrent.week_day in range(1, 8):
        raise HTTPException(status_code=400, detail='Week value not valid')
    db_professional = crud_prof.get_prof_id(db, prof_id)
    if db_professional is None:
        raise HTTPException(status_code=404, detail='Professional not exist')
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    db_topic_recurrent = crud_topic_recurrent.create_recurrent(topicr, db)
    if type(db_topic_recurrent) is dict:
        raise HTTPException(status_code=400, detail=db_topic_recurrent.get('error'))
    return db_topic_recurrent

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/recurrent', tags=["Recurrent"], response_model=Union[schema_response.ResponseRecurrent, List[schema_topic_recurrent.TopicRecurrentCr1], Errors])
def get_recurrent_all(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recuperacion de todos los dias recurrentes
    """
    topicr = ProfessionalID( prof_id=prof_id)
    return crud_topic_recurrent.get_recurrent_all(topicr, db)

#@router.put('/recurrent', tags=['Recurrent'])
def update_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentUp, db:Session = Depends(get_db)):
    """
    Permite actualizar la hora de inicio y/o hora de final dado una hora de inicio

    Args:
       - prof_id: str
       - week_day: int
       - start: time <- Hora a actualizar 
       - Nstart: time | None
       - Nend: time | None
    """
    if not recurrent.week_day in range(1,8):
        raise HTTPException(status_code=400, detail='Week value invalid')
    
    topicr = schema_topic_recurrent.TopicRecurrentUpdate(**recurrent.dict(), prof_id=prof_id)
    sucess = crud_topic_recurrent.update_recurrent_time(db, topicr)

    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail':'Recurrent day updated'}

#@router.delete('/recurrent', tags=['Recurrent'])
def del_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentWeekS, db:Session = Depends(get_db)):
    """
    Eliminacion de un dia recurrente
    """
    recu = schema_topic_recurrent.TopicRecurrentSchema(**recurrent.dict(), prof_id= prof_id)
    sucess = crud_topic_recurrent.delete_recurrent(db, recu)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail': 'Recurrent day deleted'}




@router.post('/topic', tags=['Recurrent'])
def add_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Agrega un topico a un dia recurrente particular
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id=prof_id)
    sucess = crud_topic_recurrent.add_topic_recurrent(db, recurrent_topic)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return sucess

@router.delete('/topic', tags=['Recurrent'], response_model=Union[Info, Errors])
def del_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Elimina un topico de un dia recurrente
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id= prof_id)
    sucess = crud_topic_recurrent.del_topic_recurrent(db, recurrent_topic)
    if type(sucess) is dict:
        raise HTTPException(status_code=400, detail=sucess.get('error'))
    return {'detail': 'Deleted Topic from Recurrent'}




