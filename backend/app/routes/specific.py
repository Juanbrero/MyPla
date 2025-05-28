from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time
from ..controllers.SpecificController import SpecificController

from app.bd.schemas import schema_topic_recurrent,  schema_response, schema_topic_specific, schema_specific , schema_prof
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from app.bd.bd_utils import Errors, Info

router = APIRouter(prefix="/specific")

@router.post('',tags=["Specific"], response_model=Union[schema_topic_specific.TopicSpecificIn, Errors])
def create_specific_day(prof_id:str, specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db)):
    """
    Creacion de un dia especifico
    """
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= prof_id, isCanceling= False)
    return SpecificController(db=db).createSpecific(topicS)

@router.get('',tags=["Specific"],response_model=Union[schema_response.ResponseSpecific, List[schema_topic_specific.TopicSpecificCr1], Errors])
def get_specific(prof_id:str,  db:Session = Depends(get_db)):
    """
    Recupercion de todos los dias especificos de un profesional
    """
    return SpecificController(db=db).getAllSpecifics(prof_id)

@router.put('',tags=["Specific"],response_model=Union[schema_topic_specific.TopicSpecificUpdate, Errors])
def update_specific(prof_id:str, specific:schema_topic_specific.TopicSpecificDay,  db:Session = Depends(get_db)):
    """
    Actualizar dia especifico de un profesional
    """
    
    topicS = schema_topic_specific.TopicSpecificUpdate(**specific.dict(), prof_id= prof_id)
    return SpecificController(db=db).updateSpecific(topicS)

@router.delete('',tags=["Specific"],response_model=Union[schema_topic_specific.TopicSpecificDeleteIn, Errors])
def delete_specific(prof_id:str, specific:schema_topic_specific.TopicSpecificDeleteCtrl,  db:Session = Depends(get_db)):
    """
    Actualizar dia especifico de un profesional
    """
    
    topicS = schema_topic_specific.TopicSpecificDeleteIn(**specific.dict(), prof_id= prof_id)
    return SpecificController(db=db).deleteSpecific(topicS)