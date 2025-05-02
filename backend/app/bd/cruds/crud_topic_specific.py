from sqlalchemy.orm import Session
from app.models import TopicSpecific, SpecificSchedule
from app.bd.schemas import schema_topic_specific, schema_specific, schema_topic
from sqlalchemy import insert, update, delete, select

from ..bd_utils import strip_time_hour_minute, valid_time, include_time
from ..bd_exceptions import MinuteError, CompleteHour

#USAR ESTA
#Creacion con validaciones, manejo de errores propios y errores mas claros
def create2(topicS:schema_topic_specific.TopicSpecificIn, db:Session):
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

    
#ESTE
#Recupera TODOS los dias especificos de un profesional ID,
#Solo aquellos que no sean cancelaciones y por eso posee topicos asociados
def get2(topicS:schema_topic_specific.TopicSpecificSchema, db:Session):
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
        return respuesta
    except:
        return {'error':' - error'}

#Funcion que recupera todos los inicio y fin de el dia especificado
def __get_schedule(db: Session, specific:schema_specific.SpecificSchema):
    smt = select(SpecificSchedule).where(SpecificSchedule.prof_id == specific.prof_id, SpecificSchedule.day == specific.day)
    response = db.scalars(smt).all()
    return response


##
#Solo recibe un topico y lo agrega
def create(topicS: schema_topic_specific.TopicSpecificCreate, db:Session):
    topicS.start = strip_time_hour_minute(topicS.start)
    try:
        smt = insert(TopicSpecific).values(topicS.dict())
        response = db.execute(smt)
        db.commit()
        return topicS
    except:
        return {'error':'not possible insert'}

#Recuperacion muy especifica No muy util    
def get(topicS: schema_topic_specific.TopicSpecificSchema, db:Session):
    topicS.start = strip_time_hour_minute(topicS.start)
    try:
        smt = select(TopicSpecific).where(topicS.prof_id == TopicSpecific.prof_id, 
                                           topicS.start == TopicSpecific.start, 
                                           topicS.day == TopicSpecific.day)
        response = db.scalars(smt).all()
        return response
    except:
        return {'error':'no se puedo recuperar datos'}
    

#Recibe todo el JSON con los topicos en un vector, solo try en el sql
def create1(topicS:schema_topic_specific.TopicSpecificIn, db:Session):
    topicS.start = strip_time_hour_minute(topicS.start)
    topicS.end = strip_time_hour_minute(topicS.end)
    topicS.topics = [ {'topic_name':r.dict()['topic_name'].upper()} for r in topicS.topics ]
    spec = schema_specific.SpecificSchema(**topicS.dict())
    try:
        smt = insert(SpecificSchedule).values(spec.dict())
        db.execute(smt)
        for r in topicS.topics:
            ins = schema_topic_specific.TopicSpecificCreate(**topicS.dict(), topic_name=r['topic_name'])
            smt = insert(TopicSpecific).values(ins.dict())
            result = db.execute(smt)
        db.commit()
        return topicS
    except:
        return {'error':'error'}
    
#Recupera un dia, hora ID, especifico, no muy util 
#Al ser tan especifico y manejar hora se hace una transformacion, sin el try para controlar
def get1(topicS:schema_topic_specific.TopicSpecificSchema, db:Session):
    topicS.start = strip_time_hour_minute(topicS.start) 
    try:
        smt = select(TopicSpecific.topic_name).where(TopicSpecific.prof_id == topicS.prof_id, 
                                                      TopicSpecific.start == topicS.start, 
                                                      TopicSpecific.day == topicS.day)
        response = db.scalars(smt).all()
        smte = select(SpecificSchedule.end).where(SpecificSchedule.prof_id == topicS.prof_id, 
                                                      SpecificSchedule.start == topicS.start, 
                                                      SpecificSchedule.day == topicS.day)
        end = db.scalars(smte).first()
       
        topics_list = [{'topic_name':t} for t in response]
        respuesta = schema_topic_specific.TopicSpecificIn(**topicS.dict(), topics=topics_list, end=end)
        return respuesta
    except:
        return {'error':' - error'}

