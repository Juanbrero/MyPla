from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List

from app.bd.schemas.schema_topic import TopicCreate, Topic
from app.bd.cruds import crud_topic


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
