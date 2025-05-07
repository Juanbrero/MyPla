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


#EN PROCESO
def update_recurrent(db:Session, recurrent:schema_topic_recurrent.TopicRecurrentIn):
    week = recurrent.week_day
    prof_id = recurrent.prof_id
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
        recurrent.end = strip_time_hour_minute(recurrent.end)
    except MinuteError as e:
        return {'error':f'{e}'}
    try:
        if recurrent.week_day not in range(1,8):
            raise WeekError(recurrent.week_day)
    except WeekError as e:
        return {'error':f'{e}'}
    if valid_time(recurrent):
        response = db.query(RecurrentSchedule).filter(RecurrentSchedule.prof_id == prof_id,
                                                RecurrentSchedule.week_day == week).all()
        if len(response) == 0:
            return {'error': ' Not schedule to this week day'}
    else:
        return {'error': f'Time Start: {recurrent.start} End: {recurrent.end}'}
    Ntopics = recurrent.topics
    for res in response:
        #8-10
        # 9-13
        #Incluido en el rango almacenado
        if res.start <= recurrent.start < res.end and res.start < recurrent.end <= res.end:
            try:
                stmd = delete(TopicRecurrent).where(RecurrentSchedule.prof_id == prof_id, 
                                                RecurrentSchedule.week_day == week, 
                                                RecurrentSchedule.start == res.start)
                response = db.execute(stmd)
                ic(f'{response}')
            except:
                return {'error': 'on delete topicRecurrent'}
            try:
                stmd =  delete(RecurrentSchedule).where(RecurrentSchedule.prof_id == prof_id,
                                                        RecurrentSchedule.week_day == week,
                                                        RecurrentSchedule.start == res.start)
                response = db.execute(stmd)
            except:
                return {'error':'on delete Recurrent Schedule'}
        elif res.start <= recurrent.start < res.end and res.start < recurrent.end > res.end:
            pass
    return create_recurrent(recurrent, db)

