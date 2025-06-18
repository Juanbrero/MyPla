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
def create_topic( topicS: schema_topic.TopicCreate, db:Session = Depends(get_db)):
    """
    - Crea un topico
        - data:
            - topic_name: str (not case sensitive)
            - category_name: str (not case sensitive)
    """
    return TopicController(db= db).createTopic(topicS)

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

@router.get('/category', tags=['Topics'])
def get_via_category(category_name:str, db: Session = Depends(get_db)):
    """
    - Recupera todos los topicos de una categoria dada
        - param **category_name**
    """
    return TopicController(db= db).getTopicsCategory(category_name= category_name)

