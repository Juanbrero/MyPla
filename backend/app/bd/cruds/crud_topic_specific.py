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


#Funcion que recupera los datos que esten entre el rango
def __include(db:Session, specific:schema_specific.SpecificSchema):
    """
    Funcion para buscar inclusion en update IN PROCESS
    """
    smt = select(SpecificSchedule.start).where(SpecificSchedule.prof_id == specific.prof_id, SpecificSchedule.day == specific.day,
                                         SpecificSchedule.start <= specific.start and SpecificSchedule.end <= specific.end  )
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

# EN PROCESO
def update_specific(db:Session, specific:schema_topic_specific.TopicSpecificUpdate):
    try:
        startN = strip_time_hour_minute(specific.new['start'])
        endN = strip_time_hour_minute(specific.new['end'])
        startO = strip_time_hour_minute(specific.old['start'])
    except MinuteError as e:
        return {'error':f'{e}'}
    ic('Tiempos ajustados')
    dayN = specific.new['day']
    try:
        if valid_time(specific.new):
            spec = schema_specific.SpecificSchema(prof_id= specific.prof_id, start= startN, day= dayN, end= endN)
            exist = __include(db, spec)
            ic(f'recuperado {exist}')
            # exist seria un arreglo con los start, que estan entre new.start y new.end del new.day
            if len(exist) > 1:
                try:
                    ic('Elimando old')
                    stm = delete(SpecificSchedule).where(SpecificSchedule.day == dayN, SpecificSchedule.prof_id == specific.prof_id, SpecificSchedule.start == startO)
                    response = db.execute(stm)
                    if response.rowcount > 0:
                        try:
                            ic('eliminando colisiones new')
                            for st in exist:
                                stm= delete(SpecificSchedule).where(SpecificSchedule.day == spec.day, SpecificSchedule.prof_id == spec.prof_id, SpecificSchedule.start == st)
                                response = db.execute(stm)
                            if response.rowcount > 0:
                                try:
                                    ic('insertando update')
                                    ins = schema_topic_specific.TopicSpecificIn(**spec.dict(), topics=specific.new['topics'])
                                    return create2(ins, db)
                                except:
                                    pass
                            else:
                                return {'error': 'not posible delete Specific INCLUDE'}
                        except:
                            return {'error':'in delete Specific NEW'}
                    else:
                        return {'error': 'not posible delete Specific OLD'}
                except:
                    return {'error':'in delete Specific OLD'}
            elif len(exist) == 1:
                try:
                    for topic in specific.new:
                        pass
                except:
                    pass
    except CompleteHour as e:
        return {'error':f'{e}'}
    except:
        return {'error':'error'}


    return 
