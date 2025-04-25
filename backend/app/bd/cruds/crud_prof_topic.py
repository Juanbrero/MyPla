from sqlalchemy.orm import Session
from app.models.ProfesionalTopic import ProfesionalTopic
from app.bd.schemas import schema_prof_topic
from sqlalchemy import exc
from app.bd.bd_utils import error_hand


def add_topic(db:Session, prof_topic: schema_prof_topic.ProfesionalTopicCreate):
    try:
        db_prof_topic =ProfesionalTopic(**prof_topic.dict())
        db.add(db_prof_topic)
        db.commit()
        db.refresh(db_prof_topic)
        return db_prof_topic
    except exc.IntegrityError as e:
        error = error_hand(e)
        return {'error':f'Error al insertar, clave Foranea \n{error}'}

def get_topics(db:Session, prof_id:int):
    return db.query(ProfesionalTopic).filter(ProfesionalTopic.user_id ==  prof_id).all()
