from sqlalchemy.orm import Session
from app.models import TopicRecurrent, RecurrentSchedule
from app.bd.schemas import schema_topic_recurrent, schema_recurrent, schema_topic
from sqlalchemy import insert, update, delete, select, between

from ..bd_utils import strip_time_hour_minute, valid_time, include_time
from ..bd_exceptions import MinuteError, CompleteHour, WeekError


def create_recurrent(topicr:schema_topic_recurrent.TopicRecurrentIn, db:Session):
    """
    Crea un Recurrent y sus Topicos asociados
    Inserta en recurrent y luego los topicos en TopicReurrent

    Args:
        topicr: schema_topic_recurrent.TopicRecurrentIn
            - week_day: int [1-7]
            - start: time
            - end: time
            - prof_id: str
            - topics: [Topics]
                - topic_name: str
        db: Session
    Return:
        topicr
        {'error':}
    """
    try:
        topicr.start = strip_time_hour_minute(topicr.start)
        topicr.end = strip_time_hour_minute(topicr.end)
    except MinuteError as e:
        return {'error':f'{e}'}
    try:
        if topicr.week_day not in range(1,8):
            raise WeekError(topicr.week_day)
    except WeekError as e:
        return {'error':f'{e}'}
    
    try:
        if valid_time(topicr):
            exist = __get_schedule(db, topicr)
            if not include_time(exist, topicr):
                topicr.topics = [ {'topic_name':r.dict()['topic_name'].upper()} for r in topicr.topics ]
                recu = schema_recurrent.RecurrentSchema(**topicr.dict())
                try:
                    smt = insert(RecurrentSchedule).values(recu.dict())
                    db.execute(smt)
                    try:
                        for r in topicr.topics:
                            ins = schema_topic_recurrent.TopicRecurrentCreate(**topicr.dict(), topic_name=r['topic_name'])
                            smt = insert(TopicRecurrent).values(ins.dict())
                            db.execute(smt)
                        db.commit()
                        return topicr
                    except:
                        return {'error':'on insert in TopicRecurrent'}
                except:
                    return {'error': 'on insert in recurrent'}
            else:
                return {'error': 'time include in DB'}
        else:
            return {'error': f'Error hour {topicr.start} == {topicr.end}'}    
    except CompleteHour as e:
        return {'error':f'{e}'}
    except:
        return {'error':'error'}

    

def get_recurrent(topicr:schema_topic_recurrent.TopicRecurrentSchema, db:Session):
    """
    Recupera todos los topicos de un professional dado
    Args:
        topicr: schema_topic_recurrent.TopicRecurrentSchema
            - prof_id
            - week_day <- No usado
            - start  <- no usado
    Return
        {'recurrent': [{schema_topic_recurrent.TopicRecurrentCr1}]}
            - week_day:
            - start:
            - end:
            - topics: [Topics]
        {'error':}
    """
    respuesta = []
    try:
        smt = select(RecurrentSchedule).where(RecurrentSchedule.prof_id == topicr.prof_id)
        response = db.scalars(smt).all()
    except:
        {'error':'in select recurrent'}
    try:
        for r in response:
            smt = select(TopicRecurrent.topic_name).where(TopicRecurrent.prof_id == r.prof_id, 
                                                      TopicRecurrent.start == r.start, 
                                                      TopicRecurrent.week_day == r.week_day)
            response = db.scalars(smt).all() #[{a, 20:30, 2, INGLES}, {a, 20:30, 2, FRANCES}]
            topics_list = [{'topic_name':t} for t in response]
            respuesta.append( schema_topic_recurrent.TopicRecurrentCr1(end=r.end, start=r.start, week_day=r.week_day, topics=topics_list))
        return {'recurrent':respuesta}
    except:
        return {'error':' - error'}
    

def delete_recurrent(db:Session, recurrent:schema_topic_recurrent.TopicRecurrentSchema):
    """
    Elimina un dia concurrente junto a sus topicos asociados

    Args:
        topicr: schema_topic_recurrent.TopicRecurrentSchema
            - prof_id
            - week_day 
            - start  
        db: Session
    Return:
        {'info':}
        {'error':}
    """
    recurrent.start = strip_time_hour_minute(recurrent.start)
    try:
        stm = delete(TopicRecurrent).where(RecurrentSchedule.prof_id == recurrent.prof_id, 
                                           RecurrentSchedule.start == recurrent.start, 
                                           RecurrentSchedule.week_day == recurrent.week_day )
        response = db.execute(stm)
        try:
            if response.rowcount > 0:
                stm = delete(RecurrentSchedule).where(RecurrentSchedule.prof_id == recurrent.prof_id,
                                                       RecurrentSchedule.start == recurrent.start,
                                                         RecurrentSchedule.week_day == recurrent.week_day )
                response = db.execute(stm)
                if response.rowcount > 0:
                    db.commit()
                    return {'info': f'Delete {recurrent.dict()}'}
                else:
                    raise
            else:
                return {'error': 'Calendario recurrente ya elimiando'}
        except:
            return {'error': 'on delete recurrent'}
    except:
        return {'error':'in delte topic_recurrent'}
        

#Recupera todos los datos de un profesional en un dia de semana particular
def __get_schedule(db: Session, recurrent:schema_recurrent.RecurrentSchema):
    """
    Recupera todos los dias recurrentes de un profesional en un dia de semana particular
    Usado para definir inclusion

    Args:
        db: Session
        recurrent: schema_recurrent.RecurrentSchema
            - prof_id: str
            - week_day: date
    Return:
        [RecurrentSchedule]
    """

    smt = select(RecurrentSchedule).where(RecurrentSchedule.prof_id == recurrent.prof_id,
                                           RecurrentSchedule.week_day == recurrent.week_day)
    response = db.scalars(smt).all()
    return response

def add_topic_recurrent(db:Session, recurrent:schema_topic_recurrent.TopicRecurrentCreate):
    """
    Agrega un topico a un dia recurrente existente

    Args:
        recurrent:
            - prof_id: str
            - week_day: int
            - start: time
            - topic_name: str
    
    """
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    recurrent.topic_name = recurrent.topic_name.upper()
    try:
        response = db.query(RecurrentSchedule).filter(RecurrentSchedule.start == recurrent.start, 
                                                        RecurrentSchedule.prof_id == recurrent.prof_id,
                                                        RecurrentSchedule.week_day == recurrent.week_day).first()
        if response is None:
            return {'error': 'recurrent day not exist'}
    except:
        return {'error': 'On select recurrent'}
    try:
        db_topic = TopicRecurrent(**recurrent.dict())
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        return db_topic
    except:
        return {'error': 'On insert Topic in Recurrent'}

def del_topic_recurrent(db:Session, recurrent:schema_topic_recurrent.TopicRecurrentCreate):
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    recurrent.topic_name = recurrent.topic_name.upper()
    try:
        response = db.query(TopicRecurrent).filter(TopicRecurrent.start == recurrent.start, 
                                                        TopicRecurrent.prof_id == recurrent.prof_id,
                                                        TopicRecurrent.week_day == recurrent.week_day,
                                                        TopicRecurrent.topic_name == recurrent.topic_name).first()
        if response is None:
            return {'error': 'Topic not exist'}
    except:
        return {'error': 'On select topic'}
    try:
       db.delete(response)
       db.commit()
       return {'info':'Ok delete'}
    except:
        return {'error': 'On delete Topic in Recurrent'}




#EN PROCESO
def update_recurrent_time(db:Session, recurrent:schema_topic_recurrent.TopicRecurrentUpdate):
    """
    Permite actualizar hora de inicio y final de un dia particular
    Se puede actualizar start, end o ambos

    Args:
        db: Session
        recurrent: schema_topic_recurrent.TopicRecurrentUpdate
            - prof_id: str
            - week_day: int
            - start: time -> Elemento a actualizar
            - Nstart: time | None
            - Nend: time | None
    Return:
        {'info':'OK'}
        {'error':}
    """
    if recurrent.Nstart is None and recurrent.Nend is None:
        return {'error': 'No hay update'}
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
    except MinuteError as e:
        return {'error':f'{e}'}
    try:
        if recurrent.week_day not in range(1,8):
            raise WeekError(recurrent.week_day)
    except WeekError as e:
        return {'error':f'{e}'}

    recu = db.query(RecurrentSchedule).filter(RecurrentSchedule.week_day == recurrent.week_day, 
                                              RecurrentSchedule.prof_id == recurrent.prof_id, 
                                              RecurrentSchedule.start == recurrent.start).first()
    if recu is None:
        return {'error':'Dia recurrente no existente'}
    try:
        if  not recurrent.Nstart is None:
            recu.start = strip_time_hour_minute(recurrent.Nstart)
        if not recurrent.Nend is None:
            recu.end = strip_time_hour_minute(recurrent.Nend)
    except MinuteError as e:
        return {'error':f'{e}'}
    if valid_time(recu):
        exist = db.query(RecurrentSchedule).filter(RecurrentSchedule.prof_id== recu.prof_id,
                                                    RecurrentSchedule.week_day == recu.week_day,
                                                    RecurrentSchedule.start != recurrent.start
                                                   ).all()
        if not include_time(exist, recu):
            try:    
                updates = {'start': recu.start, 'end': recu.end}        
                smt = update(RecurrentSchedule).where(RecurrentSchedule.prof_id== recurrent.prof_id,
                                                        RecurrentSchedule.start == recurrent.start,
                                                        RecurrentSchedule.week_day == recurrent.week_day).values(updates)
                db.commit()
                return {'info': 'OK'}
            except:
                return {'error':'On update Recurrent'}
        else:
            return {'error': 'time include in DB'}
    else:
        return {'error': f'Error hour {recu.start} == {recu.end}'}    