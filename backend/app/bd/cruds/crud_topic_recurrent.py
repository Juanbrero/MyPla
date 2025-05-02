from sqlalchemy.orm import Session
from app.models import TopicRecurrent, RecurrentSchedule
from app.bd.schemas import schema_topic_recurrent, schema_recurrent, schema_topic
from sqlalchemy import insert, update, delete, select

from ..bd_utils import strip_time_hour_minute, valid_time, include_time
from ..bd_exceptions import MinuteError, CompleteHour, WeekError

#ESTE USADO 
def create2(topicr:schema_topic_recurrent.TopicRecurrentIn, db:Session):
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
            return {'error': f'Same hour {topicr.start} == {topicr.end}'}    
    except CompleteHour as e:
        return {'error':f'{e}'}
    except:
        return {'error':'error'}

    
#ESTE
def get2(topicr:schema_topic_recurrent.TopicRecurrentSchema, db:Session):
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
        return respuesta
    except:
        return {'error':' - error'}

#Recupera todos los datos de un profesional en un dia de semana particular
def __get_schedule(db: Session, recurrent:schema_recurrent.RecurrentSchema):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.prof_id == recurrent.prof_id, RecurrentSchedule.week_day == recurrent.week_day)
    response = db.scalars(smt).all()
    return response


##

def create(topicr: schema_topic_recurrent.TopicRecurrentCreate, db:Session):
    topicr.topic_name = topicr.topic_name.upper()
    topicr.start = strip_time_hour_minute(topicr.start)
    try:
        smt = insert(TopicRecurrent).values(topicr.dict())
        response = db.execute(smt)
        db.commit()
        return topicr
    except:
        return {'error':'not possible insert'}
    
def get(topicr: schema_topic_recurrent.TopicRecurrentSchema, db:Session):
    topicr.start = strip_time_hour_minute(topicr.start)
    try:
        smt = select(TopicRecurrent).where(topicr.prof_id == TopicRecurrent.prof_id, 
                                           topicr.start == TopicRecurrent.start, 
                                           topicr.week_day == TopicRecurrent.week_day)
        response = db.scalars(smt).all()
        return response
    except:
        return {'error':'no se puedo recuperar datos'}
    

def create1(topicr:schema_topic_recurrent.TopicRecurrentIn, db:Session):
    topicr.start = strip_time_hour_minute(topicr.start)
    topicr.end = strip_time_hour_minute(topicr.end)
    topicr.topics = [ {'topic_name':r.dict()['topic_name'].upper()} for r in topicr.topics ]
    recu = schema_recurrent.RecurrentSchema(**topicr.dict())
    try:
        smt = insert(RecurrentSchedule).values(recu.dict())
        db.execute(smt)
        for r in topicr.topics:
            ins = schema_topic_recurrent.TopicRecurrentCreate(**topicr.dict(), topic_name=r['topic_name'])
            smt = insert(TopicRecurrent).values(ins.dict())
            db.execute(smt)
        db.commit()
        return topicr
    except:
        return {'error':'error'}


def get1(topicr:schema_topic_recurrent.TopicRecurrentSchema, db:Session):
    topicr.start = strip_time_hour_minute(topicr.start) 
    try:
        smt = select(TopicRecurrent.topic_name).where(TopicRecurrent.prof_id == topicr.prof_id, 
                                                      TopicRecurrent.start == topicr.start, 
                                                      TopicRecurrent.week_day == topicr.week_day)
        response = db.scalars(smt).all()
        smte = select(RecurrentSchedule.end).where(RecurrentSchedule.prof_id == topicr.prof_id, 
                                                      RecurrentSchedule.start == topicr.start, 
                                                      RecurrentSchedule.week_day == topicr.week_day)
        end = db.scalars(smte).first()
       
        topics_list = [{'topic_name':t} for t in response]
        respuesta = schema_topic_recurrent.TopicRecurrentIn(**topicr.dict(), topics=topics_list, end=end)
        return respuesta
    except:
        return {'error':' - error'}
