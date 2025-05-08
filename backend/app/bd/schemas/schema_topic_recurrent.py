from pydantic import BaseModel
from datetime import time
from .schema_topic import Topic
from typing import Optional
#Aqui van los esqueletos de respuestas que podran obtener


#Esquema para pedir en insert
class TopicRecurrentBase(BaseModel):
    week_day: int
    start:time
    topic_name: str

#Esquema que se envia al crud
class TopicRecurrentCreate(TopicRecurrentBase):
    prof_id:str

#Respuesta get
class TopicRecurrent(BaseModel):
    topic_name:str
    
    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True


class TopicRecurrentCr1(BaseModel):
    week_day: int
    start: time
    end: time
    topics: list[Topic]

class TopicRecurrentIn(TopicRecurrentCr1):
    prof_id: str

class TopicRecurrentID(BaseModel):
    prof_id:str

class TopicRecurrentWeekS(BaseModel):
    week_day: int
    start: time

class TopicRecurrentSchema(TopicRecurrentID):
    week_day: int
    start: time


class TopicRecurrentUp(TopicRecurrentWeekS):
    Nstart: Optional[time]
    Nend: Optional[time]

class TopicRecurrentUpdate(TopicRecurrentUp, TopicRecurrentID):
    pass
