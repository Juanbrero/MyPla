from sqlalchemy.orm import Session
from app.models.ProfessionalTopic import ProfessionalTopic
from app.bd.schemas import schema_prof_topic
from sqlalchemy import exc, delete
from app.bd.bd_utils import error_hand


def add_topic(db:Session, prof_topic: schema_prof_topic.ProfessionalTopicCreate):
    if prof_topic.price_class <= 0:
        return {'error':'Price incorrect'}
    try:
        db_prof_topic = ProfessionalTopic(**prof_topic.dict())
        db.add(db_prof_topic)
        db.commit()
        db.refresh(db_prof_topic) # <- Aca falla al no poder refrescar con los datos
        return db_prof_topic
    except exc.IntegrityError as e:
        error = error_hand(e)
        return {'error':f'Error al insertar \n{error}'}

def get_topics(db:Session, prof_topic:schema_prof_topic.ProfessionalTopicID):
    return db.query(ProfessionalTopic).filter(ProfessionalTopic.prof_id ==  prof_topic.prof_id).all()


def del_topic_professional(db:Session, topic:schema_prof_topic.ProfessionalTopicDel):
    try:
        smt = delete(ProfessionalTopic).where(ProfessionalTopic.topic_name == topic.topic_name.upper(), ProfessionalTopic.prof_id == topic.prof_id)
        db.execute(smt)
        db.commit()
    except:
        return {'error': f'On delete {topic}'}
    return topic
