from sqlalchemy.orm import Session
from app.models.ProfessionalTopic import ProfessionalTopic
from app.bd.schemas import schema_prof_topic, schema_prof
from sqlalchemy import exc, delete, update
from app.bd.bd_utils import error_hand


def add_topic(db:Session, prof_topic: schema_prof_topic.ProfessionalTopic):
    """
    Funcion que agrega un topico a un profesionnal
    
    Args:
        db (Session): Database conection
        prof_topic (schema_prof_topic.ProfessionalTopicCreate)
            - topic_name: str
            - price_class: float
            - prof_id: str
    Returns:
        {prof_id:, topic_name:, price_class:} ProfessionalTopic
        {'error':}
    """
    if prof_topic.price_class <= 0:
        return {'error':'Price invalid > 0'}
    try:
        db_prof_topic = ProfessionalTopic(**prof_topic.dict())
        db.add(db_prof_topic)
        db.commit()
        db.refresh(db_prof_topic) # <- Aca falla al no poder refrescar con los datos
        return db_prof_topic
    except exc.IntegrityError as e:
        error = error_hand(e)
        return {'error':f'Error al insertar \n{error}'}

def get_topics(db:Session, prof_topic:schema_prof.ProfessionalID):
    """
    Funcion que recupera todos los topicos y precios de un profesional

    Args:
        db (Session): Database conection
        prof_topic (schema_prof.ProfessionalID)
            - prof_id: str
    Returns:
        [{prof_id:, topic_name:, price_class:}] [ProfessionalTopic]
        []
    """
    return db.query(ProfessionalTopic).filter(ProfessionalTopic.prof_id ==  prof_topic.prof_id).all()


def del_topic_professional(db:Session, topic:schema_prof_topic.ProfessionalTopicDel):
    """
    Funcion que elimina un topico de un profesional 
    
    Args:
        db (Session): Database conection
        prof_topic (schema_prof_topic.ProfessionalTopicDel)
            - topic_name: str
            - prof_id: str
    Returns:
        {prof_id:, topic_name:} ProfessionalTopic
        {'error':}
    """
    try:
        smt = delete(ProfessionalTopic).where(ProfessionalTopic.topic_name == topic.topic_name.upper(), 
                                              ProfessionalTopic.prof_id == topic.prof_id)
        db.execute(smt)
        db.commit()
    except:
        return {'error': f'On delete {topic}'}
    return {'info':'Sucess delete'}

def update_price(db:Session, prof_topic:schema_prof_topic.ProfessionalTopic):
    """
    Funcion que actualiza los precios de un topico de un profesional
    """

    if prof_topic.price_class <= 0:
        return {'error':'Price invalid > 0'}
    prof_topic.topic_name = prof_topic.topic_name.upper()
    try:
        response = db.query(ProfessionalTopic).filter(ProfessionalTopic.prof_id == prof_topic.prof_id,
                                        ProfessionalTopic.topic_name == prof_topic.topic_name).first()
        if response is None:
            return {'error': 'Information not exist'}

        updates = {'price_class':prof_topic.price_class}
        stm = update(ProfessionalTopic).where(ProfessionalTopic.prof_id == prof_topic.prof_id,
                                        ProfessionalTopic.topic_name == prof_topic.topic_name).values(updates)
        db.execute(stm)
        db.commit()
        return {'info': 'Price updated'}
    except:
        return {'error': 'Not possible update'}