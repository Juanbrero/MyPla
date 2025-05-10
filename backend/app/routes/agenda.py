from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time

from app.bd.schemas import schema_topic_recurrent,  schema_response, schema_topic_specific, schema_specific , schema_prof
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from app.bd.bd_utils import Errors, Info


router = APIRouter(prefix="/professionals/{prof_id}/agenda")



#RECURRENT
#Crea el recurrent, con los topicos
@router.post('/recurrent',tags=["Recurrent"], response_model=Union[schema_topic_recurrent.TopicRecurrentIn, Errors])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.create_recurrent(topicr, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/recurrent', tags=["Recurrent"], response_model=Union[schema_response.ResponseRecurrent, List[schema_topic_recurrent.TopicRecurrentCr1], Errors])
def get_recurrent(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recuperacion de todos los dias recurrentes
    """
    topicr = schema_prof.ProfessionalID( prof_id=prof_id)
    return crud_topic_recurrent.get_recurrent(topicr, db)

@router.delete('/recurrent', tags=['Recurrent'], response_model=Union[Info, Errors])
def del_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentWeekS, db:Session = Depends(get_db)):
    """
    Eliminacion de un dia recurrente
    """
    recu = schema_topic_recurrent.TopicRecurrentSchema(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.delete_recurrent(db, recu)


@router.put('/recurrent', tags=['Recurrent'], response_model=Union[Info, Errors])
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
    topicr = schema_topic_recurrent.TopicRecurrentUpdate(**recurrent.dict(), prof_id=prof_id)
    return crud_topic_recurrent.update_recurrent_time(db, topicr)


@router.post('/recurrent/topic', tags=['Recurrent'], response_model=Union[schema_topic_recurrent.TopicRecurrentCreate, Errors])
def add_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Agrega un topico a un dia recurrente particular
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id=prof_id)
    return crud_topic_recurrent.add_topic_recurrent(db, recurrent_topic)

@router.delete('/recurrent/topic', tags=['Recurrent'], response_model=Union[Info, Errors])
def del_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Elimina un topico de un dia recurrente
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.del_topic_recurrent(db, recurrent_topic)



#SPECIFIC

#Crea el dia disponible especifico, con los topicos
@router.post('/specific',tags=["Specific"], response_model=Union[schema_topic_specific.TopicSpecificIn, Errors])
def create_specific_day(prof_id:str, specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia especifico
    """
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= prof_id, isCanceling= False)
    return crud_topic_specific.create_specific(topicS, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/specific',tags=["Specific"],response_model=Union[schema_response.ResponseSpecific, List[schema_topic_specific.TopicSpecificCr1], Errors])
def get_specific(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recupercion de todos los dias especificos de un profesional
    """
    topicS = schema_prof.ProfessionalID( prof_id= prof_id)
    return crud_topic_specific.get_specific(topicS, db)



@router.get('/specific/{month}', tags=["TEST", 'Specific'], response_model=Union[schema_response.ResponseSpecific,Errors] ,summary='Codigo que recupera todos los dias (Especificos) de un profesional en un mes determinado')
def test(prof_id:str, month:int, db:Session = Depends(get_db)):
    """
    # On agenda

    ## Prueba de recuperación de los dias especificos dado un mes
    - month: int(1-12)
    - prof_id: str
    """
    topic = schema_topic_specific.TopicSpecificMonth(prof_id=prof_id, month=month)
    return crud_topic_specific.get_id_month(topic, db)


@router.put('/specific', tags=['Specific'], response_model=Union[Info, Errors])
def update_specific(prof_id:str, update:schema_topic_specific.TopicSpecificDay, db:Session = Depends(get_db)):
    spec = schema_topic_specific.TopicSpecificUpdate(**update.dict(), prof_id=prof_id)
    return crud_topic_specific.update_specific(db, spec)

@router.post('/specific/topic/', tags=['Specific'], response_model=Union[schema_topic_specific.TopicSpecificCreate, Errors])
def add_specific_topic(prof_id:str, specific:schema_topic_specific.TopicSpecificBase, db:Session = Depends(get_db)):
    """
    Agrega un topico a un dia especifico particular
    """
    specific_topic = schema_topic_specific.TopicSpecificCreate(**specific.dict(), prof_id=prof_id)
    return crud_topic_specific.add_crud_topic_specific(db, specific_topic)

@router.delete('/specific/topic/', tags=['Specific'], response_model=Union[Info, Errors])
def del_specific_topic(prof_id:str, specific:schema_topic_specific.TopicSpecificBase, db:Session = Depends(get_db)):
    """
    Elimina un topico de un dia especifico
    """
    specific_topic = schema_topic_specific.TopicSpecificCreate(**specific.dict(), prof_id= prof_id)
    return crud_topic_specific.del_topic_specific(db,specific_topic)



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

@router.put('/exceptions', tags=['Exception'])
def update_exception(prof_id:str, excep:schema_specific.ExceptionUp, db:Session = Depends(get_db)):
    """
    Permite actualizar la hora de inicio y/o hora de final dado una hora de inicio

    Args:
       - prof_id: str
       - day: int
       - start: time <- Hora a actualizar 
       - Nstart: time | None
       - Nend: time | None
    """
    excepU = schema_specific.ExceptionUpdate(**excep.dict(), prof_id= prof_id)
    return crud_specific.update_exception(db, excepU)



#Available

@router.get('/available', tags=['Available'], response_model=schema_response.ResponseProfessional)
def get_available(prof_id:str, db:Session = Depends(get_db)):
    """
    Petición de todos los horarios de un Profesional, para si mismo.

    - Args:
        - prof_id: str
    - Return:
        - {recurrent:[{}], 
        specific: [{}], 
          exception: [{}], 
          event: [{}], 
          clase: [{}]}
    """
    id= schema_prof.ProfessionalID(prof_id= prof_id )
    recurrent= crud_topic_recurrent.get_recurrent(id, db).get('recurrent')
    
    specific= crud_topic_specific.get_specific(id, db).get('specific')
    exception= crud_specific.get_exception(db, id).get('exception')
    clase = []
    event = []
    avaible = schema_response.ResponseProfessional(recurrent=recurrent,  
                                                   specific=specific,
                                                     exception=exception,
                                                     clase=clase,
                                                     event=event )
    return avaible