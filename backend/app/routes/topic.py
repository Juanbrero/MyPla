from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas import  schema_topic

from app.bd.bd_utils import Errors, Info
from app.controllers.TopicController import TopicController

router = APIRouter(prefix="/api/topics")


@router.post("", response_model= str,
              tags=["Topics"])
def create_topic( topic: str, db:Session = Depends(get_db)):
    """
    Crea un topico
    - topic_name: str (not case sensitive)
    """
    return TopicController(db= db).createTopic(topic)

@router.get("",
            response_model=List[str], tags=["Topics"])
def get_topic(db:Session = Depends(get_db)):
    """
    Recupera todos los topicos
    """
    return TopicController(db= db).getTopics()

@router.delete('', tags=['Topics'], response_model=str)
def delete_topic(topic_name:str, db:Session = Depends(get_db)):
    """
    Elimina un topico
    - topic_name: str ( not case sensitive)
    """
    return TopicController(db= db).deleteTopic(topic_name)



