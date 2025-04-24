from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.RecurrentSchedule import RecurrentSchedule

from app.bd.schemas import schema_recurrent
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date
from app.bd.bd_utils import strip_time_hour_minute, valid_time, include_time, MinuteError, test_time

from app.bd.schemas import  schema_topic, schema_prof_topic
from app.bd.cruds import crud_prof_topic
from app.models.ProfesionalTopic import ProfesionalTopic


def get_all_recurrent(db: Session, user_id:int):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.user_id == user_id)
    response = db.scalars(smt).all()
    return response


def create_recurrent(db: Session, recurrent: schema_recurrent.RecurrentCreate, id_prof:int):#, topics:list[schema_topic.Topic]):
    try:
        recurrent.start = strip_time_hour_minute(recurrent.start)
        recurrent.end = strip_time_hour_minute(recurrent.end)
        if valid_time(recurrent.start, recurrent.end):
            #topic_list = __get_topics(db, id_prof)
            existent = __get_schedule(db, id_prof, recurrent.name_day)
            if not include_time(existent, recurrent.start, recurrent.end):
                try:
                    db_spec = RecurrentSchedule(**recurrent.dict(), user_id=id_prof)
                    db.add(db_spec)
                    #crud_topic_recurrent.create(db, db_spec, topics, topic_list)
                    db.commit()
                    db.refresh(db_spec)
                except:
                    db_spec = {'error':'on create_recurent'}
                return db_spec
            else:
                return {'error':'time include in DB'}
    except MinuteError:
        return {'error':'minute accept 00 or 30'}
    return {'error': 'invalid time'}

def get_day(db: Session, id_prof:int, name_day:str):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.name_day == name_day).where(RecurrentSchedule.user_id == id_prof)
    response = db.scalars(smt).all()
    return response


def __get_topics(db:Session, id_prof:int):
    topics: ProfesionalTopic = crud_prof_topic.get_topics(db, id_prof)
    topic_list = []
    for t in topics:
        topic_list.append(t.topic_name)
    return topic_list

def __get_schedule(db: Session, id_prof:int, name_day:str):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.user_id == id_prof).where(RecurrentSchedule.name_day == name_day)
    response = db.scalars(smt).all()
    return response
