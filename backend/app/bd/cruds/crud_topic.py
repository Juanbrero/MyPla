from sqlalchemy.orm import Session
from app.models.Topic import Topic
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from app.bd.schemas import schema_topic 
from sqlalchemy import select


def create_topic(db:Session, topic:schema_topic.TopicCreate):
    topic.topic_name = topic.topic_name.upper()
    try:
        db_topic = Topic(**topic.dict())
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
    except:
        return {'Error':'On create topic'}
    return db_topic

def get_all_topic(db:Session):
    return db.query(Topic).all()

def get_topic(db:Session, topic:str):
    topic = topic.upper()
    smt = select(Topic).where(Topic.topic_name == topic)
    response = db.scalars(smt).all()
    return response