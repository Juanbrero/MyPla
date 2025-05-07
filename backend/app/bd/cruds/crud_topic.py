from sqlalchemy.orm import Session
from app.models.Topic import Topic
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from app.bd.schemas import schema_topic 
from sqlalchemy import select, exc
from ..bd_utils import error_hand

def create_topic(db:Session, topic:schema_topic.TopicCreate):
    """
    Crea un topico
    
    Args:
        db (Session): Database conection
        topic (schema_topic.TopicCreate)
            - topic_name: str -> upper()
    Returns:
        { topic_name:} Topic
        {'error':}
    """
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
    """
    Retorna todos los topicos

    Args:
        db (Session): Database conection
    Returns:
        [{ topic_name:}] Topic
        []
    """
    return db.query(Topic).all()

def delete_topic(db:Session, topic:schema_topic.TopicCreate):
    """
    Elimina un topicos

    Args:
        db (Session): Database conection
        topic (schema_topic.TopicCreate)
            - topic_name: str -> upper()
    Returns:
        {'info':} 
        {'error':}
    """
    topic.topic_name = topic.topic_name.upper()
    response = db.query(Topic).filter(Topic.topic_name == topic.topic_name).first()
    if response is None:
        {'error': 'Topico no existente'}
    db.delete(response)
    db.commit()
    return {'info':' EXIT DELETE'}