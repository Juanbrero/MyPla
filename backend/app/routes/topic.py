from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List

from app.bd.schemas.schema_topic import TopicCreate, Topic
from app.bd.cruds import crud_topic, crud_prof_topic
from app.bd.schemas.schema_prof_topic import ProfesionalTopicCreate, ProfesionalTopic



router = APIRouter(prefix="/topics",tags=["Topics"])


@router.post("/create", response_model=Topic)
def create_topic( topic:TopicCreate, db:Session = Depends(get_db)):
    return crud_topic.create_topic(db, topic)

@router.get("/get",response_model=List[Topic])
def get_topic(db:Session = Depends(get_db)):
    return crud_topic.get_all_topic(db)

@router.get("/get/{topic_name}", response_model=List[Topic])
def get_one_topic(topic_name:str, db: Session = Depends(get_db)):
    return crud_topic.get_topic(db, topic_name)


@router.post("/{topic_name}/prof/{prof_id}",response_model=ProfesionalTopic, tags=["Prof Topic"])
def add_topic(topic_name:str, prof_id:int, db: Session = Depends(get_db)):
    prof_topic = ProfesionalTopic(topic_name=topic_name.upper(), user_id=prof_id)
    return crud_prof_topic.add_topic(db,prof_topic)

@router.get("/prof/{prof_id}",response_model=List[ProfesionalTopic], tags=["Prof Topic"])
def get_topics(prof_id:int, db:Session =Depends(get_db)):
    return crud_prof_topic.get_topics(db, prof_id)