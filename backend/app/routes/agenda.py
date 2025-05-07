from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time

from app.bd.schemas import schema_topic_recurrent,  schema_response, schema_topic_specific, schema_specific
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from app.bd.bd_utils import Errors, Info


router = APIRouter(prefix="/prof/{prof_id}/agenda")


#SPECIFIC

#Crea el dia disponible especifico, con los topicos
@router.post('/create/spec',tags=["Specific"], response_model=Union[schema_topic_specific.TopicSpecificIn, Errors])
def create_specific_day(prof_id:str, specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia especifico
    """
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= prof_id, isCanceling= False)
    return crud_topic_specific.create_specific(topicS, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/get/spec',tags=["Specific"],response_model=Union[schema_response.ResponseSpecific, List[schema_topic_specific.TopicSpecificCr1], Errors])
def get_specific(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recupercion de todos los dias especificos de un profesional
    """
    topicS = schema_topic_specific.TopicSpecificID( prof_id= prof_id)
    return crud_topic_specific.get_specific(topicS, db)



@router.get('/get/specific/month', tags=["TEST", 'Specific'], response_model=Union[schema_response.ResponseSpecific,Errors] ,summary='Codigo que recupera todos los dias (Especificos) de un profesional en un mes determinado')
def test(prof_id:str, month:int, db:Session = Depends(get_db)):
    """
    # On agenda

    ## Prueba de recuperación de los dias especificos dado un mes
    - month: int(1-12)
    - prof_id: str
    """
    topic = schema_topic_specific.TopicSpecificMonth(prof_id=prof_id, month=month)
    return crud_topic_specific.get_id_month(topic, db)

#En proceso de implemantar
#@router.put('/update/specific', tags=['Specific'])
def update_specific(prof_id:str, update:schema_topic_specific.TopicSpecificON, db:Session = Depends(get_db)):
    spec = schema_topic_specific.TopicSpecificUpdate(**update.dict(), prof_id=prof_id)
    return crud_topic_specific.update_specific(db, spec)



#Exception
#crear excepciones, iscanceling= True
@router.post('/exceptions', tags=["Exception"], response_model=Union[schema_specific.ExceptionGet, Errors])
def create_exception(prof_id:str, excep:schema_specific.ExceptionBase, db: Session = Depends(get_db)):
    """
    Creacion de una excepcion
    """
    excepcion = schema_specific.ExceptionCreate(**excep.dict(), prof_id= prof_id)
    return crud_specific.create_exception(db, excepcion)

@router.get('/exceptions', tags=["Exception"], response_model=Union[schema_response.ResponseException, Errors])
def get_exception(prof_id:str, day:date, db: Session = Depends(get_db)):
    """
    Funcion que por el momento, ignora el dia, el objetivo sera utilizarlo
    - prof_id:str
    - day: date (yyyy-mm-dd) 2025-01-23 <- IGNORADO PARA EL GET, pero debe ser valida
    """
    excepcion = schema_specific.ExceptionGetDat(prof_id= prof_id, day=day)
    return crud_specific.get_exception(db, excepcion)


@router.delete('/exceptions', tags=['Exception'], response_model=Union[Errors, Info])
def del_exception(prof_id:str, excep:schema_specific.ExceptionDelDat, db:Session = Depends(get_db)):
    """
    Eliminación de una excepcion
    """
    excepD = schema_specific.ExceptionDel(**excep.dict(), prof_id=prof_id)
    return crud_specific.delete_exception(db, excepD)



#RECURRENT
#Crea el recurrent, con los topicos
@router.post('/create/recurrent',tags=["Recurrent"], response_model=Union[schema_topic_recurrent.TopicRecurrentIn, Errors])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.create_recurrent(topicr, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/get/recurrent', tags=["Recurrent"], response_model=Union[schema_response.ResponseRecurrent, List[schema_topic_recurrent.TopicRecurrentCr1], Errors])
def get_recurrent(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recuperacion de todos los dias recurrentes
    """
    topicr = schema_topic_recurrent.TopicRecurrentID( prof_id=prof_id)
    return crud_topic_recurrent.get_recurrent(topicr, db)

@router.delete('/del/recurrent', tags=['Recurrent'])
def del_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentWeekS, db:Session = Depends(get_db)):
    """
    Eliminacion de un dia recurrente
    """
    recu = schema_topic_recurrent.TopicRecurrentSchema(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.delete_recurrent(db, recu)

#En proceso de implementar
#@router.put('/update/recurrent', tags=['Recurrent'])
def update_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(),prof_id=prof_id)
    return crud_topic_recurrent.update_recurrent(db, topicr)
