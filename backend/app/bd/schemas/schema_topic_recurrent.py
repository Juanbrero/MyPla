from pydantic import BaseModel
from datetime import time, date
from .schema_topic import Topic
from .schema_prof import ProfessionalID
from typing import Optional
#Aqui van los esqueletos de respuestas que podran obtener


#Esquema para pedir en insert
class TopicRecurrentBase(BaseModel):
    """
    Esquema para agregar/ eliminar un topicos
        - week_day: int
        - start:time
        - topic_name: str

    """
    week_day: int
    start:time
    topic_name: str

#Esquema que se envia al crud
class TopicRecurrentCreate(TopicRecurrentBase):
    """
    Esquema que completa la informacion para agregar un topico
        - week_day: int
        - start:time
        - topic_name: str
        - prof_id: str
    """
    prof_id:str

#Respuesta get
class TopicRecurrent(BaseModel):
    topic_name:str
    
    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True


class TopicRecurrentCr1(BaseModel):
    """
    ORM
    Esquema para recibir la información para crear un dia recurrente con sus topicos
        - week_day: int
        - start:time
        - topics: list[str]
            - topic_name: str
    """
    week_day: int
    start: time
    end: time
    topics: list[str]
    class Config:
        orm_mode= True

class TopicRecurrentIn(TopicRecurrentCr1):
    """
    Esquema que se basa en TopicRecurrentCr1, agregando el prof_id, para enviar a las funciones
        - week_day: int
        - start:time
        - topics: list[Topic]
            - topic_name: str
        - prof_id: str
    """
    prof_id: str


class TopicRecurrentWeekS(BaseModel):
    """
    Esquema que posee solo el dia de la semana(int), y la hora de inicio

    """
    week_day: int
    start: time

class TopicRecurrentSchema(ProfessionalID):
    """
    Esquema que agrega al TopicRecurrentID el dia de la semana y la hora de inicio
        - prof_id: str
        - week_day: int
        - start:time
    """
    week_day: int
    start: time


class TopicRecurrentUp(TopicRecurrentWeekS):
    """
    Esquema utilizado para recibir la información para actualizar
        Se puede actualizar Nstart y/o Nend
        - week_day: int
        - start:time
        - Nstart: time | None
        - Nend: time | None
    """
    Nstart: Optional[time]
    Nend: Optional[time]

class TopicRecurrentUpdate(TopicRecurrentUp, ProfessionalID):
    """
    Esquema utilizado para realizar la actualización, basado en
        - prof_id: str
        - week_day: int
        - start:time
        - Nstart: time | None
        - Nend: time | None  
    """
    pass

class TopicRecurrentWeekGet(ProfessionalID):
    """
        - prof_id
        - week_day
    """
    week_day: int
    

class TopicRecurrentWeekRes(TopicRecurrentWeekS):
    """
     - week_day
     - start
     - end
    """
    end:time

    class Config:
        orm_mode= True


class TopicRecurrentMonthYear(ProfessionalID):
    """
    prof_id
    month: int
    year: int = today().year
    """
    month: int
    year: int = date.today().year