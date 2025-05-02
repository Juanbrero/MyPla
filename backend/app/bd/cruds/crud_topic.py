from sqlalchemy.orm import Session
from app.models.Topic import Topic
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from app.bd.schemas import schema_topic 
from sqlalchemy import select, exc
from ..bd_utils import error_hand

def create_topic(db:Session, topic:schema_topic.TopicCreate):
    topic.topic_name = topic.topic_name.upper()
    try:
        db_topic = Topic(**topic.dict())
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
    except exc.IntegrityError as e:
        error = error_hand(e)
        return {'error':f'{error} -> On create topic'}
    return db_topic

def get_all_topic(db:Session):
    return db.query(Topic).all()
