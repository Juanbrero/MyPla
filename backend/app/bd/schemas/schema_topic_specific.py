from pydantic import BaseModel
from datetime import time, date
from .schema_topic import Topic
from typing import Optional
#Aqui van los esqueletos de respuestas que podran obtener


#Esquema para pedir en insert
class TopicSpecificBase(BaseModel):
    day: date
    start:time
    topic_name: str

#Esquema que se envia al crud
class TopicSpecificCreate(TopicSpecificBase):
    prof_id:str

#Respuesta get
class TopicSpecific(BaseModel):
    topic_name:str
    
    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True

class TopicSpecificSchema(BaseModel):
    prof_id:str
    day: date
    start: time


class TopicSpecificCr1(BaseModel):
    day: date
    start: time
    end: time
    topics: list[Topic]

class TopicSpecificIn(TopicSpecificCr1):
    prof_id: str
    isCanceling: bool

class TopicSpecificID(BaseModel):
    prof_id:str

class TopicSpecificMonth(TopicSpecificID):
    month: int

class TopicSpecificDay(BaseModel):
    day: date
    start:time
    Nstart: Optional[time]
    Nend: Optional[time]

class TopicSpecificUpdate(TopicSpecificDay):
    prof_id: str