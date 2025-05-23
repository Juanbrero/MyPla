from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from ..controllers.RecurrentController import RecurrentController
from app.bd.schemas import schema_topic_recurrent

router = APIRouter(prefix="/api/professionals/{prof_id}/recurrent")



@router.post('', tags=['Recurrent'])
def create_recurrent(prof_id: str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db: Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    recurrentS = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return RecurrentController(db= db).createRecurrent(recurrentS)



#@router.post('/recurrent',tags=["Recurrent"], response_model=Union[schema_topic_recurrent.TopicRecurrentIn, Errors])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.create_recurrent(topicr, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
#@router.get('/recurrent', tags=["Recurrent"], response_model=Union[schema_response.ResponseRecurrent, List[schema_topic_recurrent.TopicRecurrentCr1], Errors])
def get_recurrent(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recuperacion de todos los dias recurrentes
    """
    topicr = schema_prof.ProfessionalID( prof_id=prof_id)
    return crud_topic_recurrent.get_recurrent(topicr, db)

#@router.delete('/recurrent', tags=['Recurrent'], response_model=Union[Info, Errors])
def del_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentWeekS, db:Session = Depends(get_db)):
    """
    Eliminacion de un dia recurrente
    """
    recu = schema_topic_recurrent.TopicRecurrentSchema(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.delete_recurrent(db, recu)


#@router.put('/recurrent', tags=['Recurrent'], response_model=Union[Info, Errors])
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


#@router.post('/recurrent/topic', tags=['Recurrent'], response_model=Union[schema_topic_recurrent.TopicRecurrentCreate, Errors])
def add_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Agrega un topico a un dia recurrente particular
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id=prof_id)
    return crud_topic_recurrent.add_topic_recurrent(db, recurrent_topic)

#@router.delete('/recurrent/topic', tags=['Recurrent'], response_model=Union[Info, Errors])
def del_recurrent_topic(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    """
    Elimina un topico de un dia recurrente
    """
    recurrent_topic = schema_topic_recurrent.TopicRecurrentCreate(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.del_topic_recurrent(db, recurrent_topic)