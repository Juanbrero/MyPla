from sqlalchemy.orm import Session
from app.models.ProfesionalTopic import ProfesionalTopic
from app.bd.schemas import schema_prof_topic



def add_topic(db:Session, prof_topic: schema_prof_topic.ProfesionalTopicCreate):
    db_prof_topic =ProfesionalTopic(**prof_topic.dict())
    db.add(db_prof_topic)
    db.commit()
    db.refresh(db_prof_topic)
    return db_prof_topic

def get_topics(db:Session, prof_id:int):
    return db.query(ProfesionalTopic).filter(ProfesionalTopic.user_id ==  prof_id).all()
