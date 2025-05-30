from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from app.bd.schemas import schema_prof_topic
from app.controllers.ProfessionalTopicController import ProfessionalTopicController
from app.auth0.dependencies import RolesValidator

router = APIRouter(prefix='/api/professionals-topic')


#PROFESSIONAL TOPIC  
@router.post("",
             response_model= str, 
             tags=["Prof Topic"])
def add_topic(prof_id: str, topic:schema_prof_topic.ProfessionalTopicCreate, db: Session = Depends(get_db)):#, user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Agregar un topico a un profesional
    """
    prof_topicS = schema_prof_topic.ProfessionalTopic(topic_name=topic.topic_name.upper(), prof_id=prof_id, price_class=topic.price_class )
    return ProfessionalTopicController(db= db).createProfTopic(prof_topicS)

@router.get("", 
            response_model=List[schema_prof_topic.ProfessionalTopic], 
            tags=["Prof Topic"])
def get_topics(prof_id: str, db:Session =Depends(get_db)):#, user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Recuperar todos los topicos de un profesional
    """
    return ProfessionalTopicController(db= db).getProfTopic(prof_id)

@router.delete('',
               tags=["Prof Topic"])
def del_topic_prof(prof_id: str, topic:str, db: Session = Depends(get_db)):#, user_info = Depends(RolesValidator(["Profesional"]))):
    """
    Elimina un topico de un profesional
    """
    prof_topicS = schema_prof_topic.ProfessionalTopicDel(topic_name= topic, prof_id=prof_id)
    return ProfessionalTopicController(db= db).deleteProfTopic(prof_topicS)

@router.put('', tags=['Prof Topic'])
def update_price_professional(prof_id: str, topic: schema_prof_topic.ProfessionalTopicCreate, db: Session = Depends(get_db)):#, user_info = Depends(RolesValidator(["Profesional"]))):
    prof_topicS = schema_prof_topic.ProfessionalTopic(**topic.dict(), prof_id=prof_id)
    return ProfessionalTopicController(db= db).updatePrice(prof_topicS)