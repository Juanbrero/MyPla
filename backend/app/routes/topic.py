from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas import  schema_topic, schema_prof_topic
from app.bd.cruds import crud_topic, crud_prof_topic
from app.bd.schemas import schema_prof_topic
from app.bd.bd_utils import Errors


router = APIRouter(prefix="/topics")
#IP/topics/get


@router.post("/create", 
             response_model=Union[schema_topic.Topic, Errors], tags=["Topics"])
async def create_topic( topic:schema_topic.TopicCreate, db:Session = Depends(get_db)):
    return crud_topic.create_topic(db, topic)

@router.get("/get",
            response_model=Union[List[schema_topic.Topic], Errors], tags=["Topics"])
async def get_topic(db:Session = Depends(get_db)):
    ic(f'GET TOPIC')
    return crud_topic.get_all_topic(db)


#PROFESSIONAL TOPIC /topic/prof 
@router.post("/prof/{prof_id}/add",
             response_model=Union[schema_prof_topic.ProfessionalTopic, Errors], 
             tags=["Prof Topic"])
async def add_topic(topic:schema_prof_topic.ProfessionalTopicCreate, prof_id:str, db: Session = Depends(get_db)):
    prof_topic = schema_prof_topic.ProfessionalTopic(topic_name=topic.topic_name.upper(), prof_id=prof_id, price_class=topic.price_class )
    return crud_prof_topic.add_topic(db, prof_topic)

@router.get("/prof/{prof_id}", 
            response_model=Union[List[schema_prof_topic.ProfessionalTopic], Errors], 
            tags=["Prof Topic"])
async def get_topics(prof_id:str, db:Session =Depends(get_db)):
    prof = schema_prof_topic.ProfessionalTopicID(prof_id=prof_id)
    return crud_prof_topic.get_topics(db, prof)

@router.delete('/prof/{prof_id}/del',
               response_model=Union[schema_prof_topic.ProfessionalTopicDel, Errors], 
               tags=["Prof Topic"])
async def del_topic_prof(prof_id:str, topic:schema_topic.TopicCreate, db: Session = Depends(get_db)):
    topics = schema_prof_topic.ProfessionalTopicDel(**topic.dict(), prof_id=prof_id)
    return crud_prof_topic.del_topic_professional(db, topics)


