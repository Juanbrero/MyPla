from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from ..controllers.SpecificController import SpecificController
from app.auth0.dependencies import RolesValidator

from app.bd.schemas import schema_response, schema_topic_specific
from app.bd.bd_utils import Errors, Info

router = APIRouter(prefix="/api/specific")

@router.post('',tags=["Specific"], response_model=Union[schema_topic_specific.TopicSpecificIn, Errors])
def create_specific_day(specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Creacion de un dia especifico
    """
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= user_info["user_id"], isCanceling= False)
    return SpecificController(db=db).createSpecific(topicS)

@router.get('',tags=["Specific"],response_model=Union[schema_response.ResponseSpecific, List[schema_topic_specific.TopicSpecificCr1], Errors])
def get_specific( db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Recupercion de todos los dias especificos de un profesional
    """
    return SpecificController(db=db).getAllSpecifics(user_info["user_id"])

@router.put('',tags=["Specific"],response_model=Union[schema_topic_specific.TopicSpecificUpdate, Errors])
def update_specific(specific:schema_topic_specific.TopicSpecificDay,  db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Actualizar dia especifico de un profesional
    """
    
    topicS = schema_topic_specific.TopicSpecificUpdate(**specific.dict(), prof_id= user_info["user_id"])
    return SpecificController(db=db).updateSpecific(topicS)

@router.delete('',tags=["Specific"],response_model=Union[schema_topic_specific.TopicSpecificDeleteIn, Errors])
def delete_specific(specific:schema_topic_specific.TopicSpecificDeleteCtrl,  db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Actualizar dia especifico de un profesional
    """
    
    topicS = schema_topic_specific.TopicSpecificDeleteIn(**specific.dict(), prof_id= user_info["user_id"])
    return SpecificController(db=db).deleteSpecific(topicS)