from sqlalchemy.orm import Session
from app.models import TopicSpecific, SpecificSchedule
from app.bd.schemas import schema_topic_specific, schema_specific, schema_topic
from sqlalchemy import insert, update, delete, select, extract

from ..bd_utils import strip_time_hour_minute, valid_time, include_time
from ..bd_exceptions import MinuteError, CompleteHour

#Creacion con validaciones, manejo de errores propios y errores mas claros
def create_specific(topicS:schema_topic_specific.TopicSpecificIn, db:Session):
    """
    Creacion de un dia especifico, con topicos

    Args:
        topicS: schema_topic_specific.TopicSpecificIn
            - day: date
            - start: time
            - end: time
            - topics: list[Topic]
                -  topic_name: str
            - prof_id: str
            - isCanceling: bool False
        db: Session
    Return:
        topicS: schema_topic_specific.TopicSpecificIn
        {'error':}
    """
    try:
        topicS.start = strip_time_hour_minute(topicS.start)
        topicS.end = strip_time_hour_minute(topicS.end)
    except MinuteError as e:
        return {'error':f'{e}'}
   
    try:
        if valid_time(topicS):
            exist = __get_schedule(db, topicS)
            if not include_time(exist, topicS):
                topicS.topics = [ {'topic_name':topic.dict()['topic_name'].upper()} for topic in topicS.topics ]
                spec = schema_specific.SpecificSchema(**topicS.dict())
                try:
                    smt = insert(SpecificSchedule).values(spec.dict())
                    db.execute(smt) # -> dia especifico {day, start, end, prof_id}
                    try:
                        for topico in topicS.topics:
                            ins = schema_topic_specific.TopicSpecificCreate(**topicS.dict(), topic_name=topico['topic_name'])
                            smt = insert(TopicSpecific).values(ins.dict())
                            db.execute(smt) # {day, start, prof_id, topic_name}
                        db.commit()
                        return topicS
                    except:
                        return {'error':'on insert in TopicSpecific'}
                except:
                    return {'error': 'on insert in specific'}
            else:
                return {'error':'time include'}
        else:
            return {'error': f'Same hour {topicS.start} == {topicS.end}'}    
    except CompleteHour as e:
        return {'error':f'{e}'}
    except:
        return {'error':'error'}

    
#Recupera TODOS los dias especificos de un profesional ID,
#Solo aquellos que no sean cancelaciones y por eso posee topicos asociados
def get_specific(topicS:schema_topic_specific.TopicSpecificSchema, db:Session):
    """
    Recupera todos los dias especificos (falta mejora para fechas)
    
    Args:
        - topicS: schema_topic_specific.TopicSpecificSchema
            -   prof_id: str
            -   day: date <- No usado
            -   start: time <- No usado
    Return:
        {'specific':[schema_topic_specific.TopicSpecificCr1]}
            -   day: date
            -   start: time
            -   end: time
            -   topics: list[Topic]
        {'error':}
    """
    respuesta = []
    try:
        smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == topicS.prof_id, SpecificSchedule.isCanceling == False)
        response = db.scalars(smt).all()
    except:
        {'error':'in select specific'}
    try:
        for r in response:
            smt = select(TopicSpecific.topic_name).where(TopicSpecific.prof_id == r.prof_id, 
                                                      TopicSpecific.start == r.start, 
                                                      TopicSpecific.day == r.day)
            response = db.scalars(smt).all() #[{a, 20:30, 2025-04-30, INGLES}, {a, 20:30, 2025-04-30, FRANCES}]
            topics_list = [{'topic_name': topic} for topic in response]
            respuesta.append( schema_topic_specific.TopicSpecificCr1(end=r.end, start=r.start, day=r.day, topics=topics_list))
        return {'specific':respuesta}
    except:
        return {'error':' - error'}

#Funcion que recupera todos los inicio y fin de el dia especificado
def __get_schedule(db: Session, specific:schema_specific.SpecificSchema):
    """
    Recuperar todos los dias de una fecha especifica, usado para 

    Args:
        db: Session
        specific: schema_specific.SpecificSchema
            - prof_id: str
            - day: date
    Return:
        [SpecificSchedule]
            - day: date
            - prof_id: str
            - start: time
            - end: end
    """
    smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == specific.prof_id, SpecificSchedule.day == specific.day)
    response = db.scalars(smt).all()
    return response


##
def get_id_month(topicS:schema_topic_specific.TopicSpecificMonth, db:Session):
    """
    Recupera todos los dias de un mes especificado

    Args:
        topicS: schema_topic_specific.TopicSpecificMonth
            - prof_id: str
            - month: int [1-12]
    Return:
        {'specific':[SpecificSchedule]}
        {'error':}
    """
    if topicS.month not in range(1,13):
        return {'error': 'Month invalid'}
    month = topicS.month
    respuesta = []
    try:
        smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == topicS.prof_id, SpecificSchedule.isCanceling == False, extract("MONTH", SpecificSchedule.day) == month )
        response = db.scalars(smt).all()
    except:
        {'error':'in select specific'}
    try:
        for r in response:
            smt = select(TopicSpecific.topic_name).where(TopicSpecific.prof_id == r.prof_id, 
                                                      TopicSpecific.start == r.start, 
                                                      extract("MONTH",TopicSpecific.day) == month)
            response = db.scalars(smt).all() #[{a, 20:30, 2025-04-30, INGLES}, {a, 20:30, 2025-04-30, FRANCES}]
            topics_list = [{'topic_name': topic} for topic in response]
            respuesta.append( schema_topic_specific.TopicSpecificCr1(end=r.end, start=r.start, day=r.day, topics=topics_list))
        return {'specific':respuesta}
    except:
        return {'error':' - error'}

def update_specific(db:Session, specific:schema_topic_specific.TopicSpecificUpdate):
    if specific.Nstart is None and specific.Nend is None:
        return {'error': 'No hay update'}

    try:
        specific.start = strip_time_hour_minute(specific.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    #CONTROL DE FECHA ANTIGUA specific.day >= today()
    
    try:
        response = db.query(SpecificSchedule).filter(SpecificSchedule.prof_id == specific.prof_id,
                                                     SpecificSchedule.day == specific.day,
                                                     SpecificSchedule.start == specific.start).first()
        if response is None:
            return {'error': 'Day not exist'}
    except:
        return {'error': 'on Select specific'}

    try:
        if  not specific.Nstart is None:
            response.start = strip_time_hour_minute(specific.Nstart)
        if not specific.Nend is None:
            response.end = strip_time_hour_minute(specific.Nend)
    except MinuteError as e:
        return {'error':f'{e}'}
    
    if valid_time(response):
        exist = db.query(SpecificSchedule).filter(SpecificSchedule.prof_id== response.prof_id,
                                                    SpecificSchedule.day == response.day,
                                                    SpecificSchedule.start != specific.start,
                                                    SpecificSchedule.isCanceling == False
                                                   ).all()
        if not include_time(exist, response):
            try:    
                updates = {'start': response.start, 'end': response.end}        
                stm = update(SpecificSchedule).where(SpecificSchedule.prof_id== specific.prof_id,
                                                        SpecificSchedule.start == specific.start,
                                                        SpecificSchedule.day == specific.day,
                                                        SpecificSchedule.isCanceling == False).values(updates)
                db.execute(stm)
                db.commit()
                return {'info': 'OK'}
            except:
                return {'error':'On update Specific'}
        else:
            return {'error': 'time include in DB'}
    else:
        return {'error': f'Error hour {response.start} == {response.end}'}    
    

def add_topic_specific(db:Session, specific:schema_topic_specific.TopicSpecificCreate):
    """
    Agrega un topico a un dia specific existente

    Args:
        recurrent:
            - prof_id: str
            - day: date
            - start: time
            - topic_name: str
    
    """
    try:
        specific.start = strip_time_hour_minute(specific.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    specific.topic_name = specific.topic_name.upper()
    try:
        response = db.query(SpecificSchedule).filter(SpecificSchedule.start == specific.start, 
                                                        SpecificSchedule.prof_id == specific.prof_id,
                                                        SpecificSchedule.day == specific.day).first()
        if response is None:
            return {'error': 'specific day not exist'}
    except:
        return {'error': 'On select specific'}
    try:
        db_topic = TopicSpecific(**specific.dict())
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        return db_topic
    except:
        return {'error': 'On insert Topic in Specific'}

def del_topic_specific(db:Session, specific:schema_topic_specific.TopicSpecificCreate):
    try:
        specific.start = strip_time_hour_minute(specific.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    specific.topic_name = specific.topic_name.upper()
    try:
        response = db.query(TopicSpecific).filter(TopicSpecific.start == specific.start, 
                                                        TopicSpecific.prof_id == specific.prof_id,
                                                        TopicSpecific.day == specific.day,
                                                        TopicSpecific.topic_name == specific.topic_name).first()
        if response is None:
            return {'error': 'Topic not exist'}
    except:
        return {'error': 'On select topic'}
    try:
       db.delete(response)
       db.commit()
       return {'info':'Ok delete'}
    except:
        return {'error': 'On delete Topic in Specific'}