from pydantic import BaseModel
from datetime import time, date
from .schema_topic import Topic
from .schema_prof import ProfessionalID
from typing import Optional
#Aqui van los esqueletos de respuestas que podran obtener



class SpecificDat(BaseModel):
    """
    - day: date
    - start: time
    """
    day: date
    start: time

class SpecificInsert(SpecificDat):
    """
    - day: date
    - start: time
    - end_time
    """
    end: time

class SpecificDaySID(SpecificDat, ProfessionalID):
    """
    - day: date
    - start: time
    - prof_id: str
    """
    pass

class SpecificSchema(SpecificDaySID):
    """
        - prof_id: str 
        - day: date
        - start: time
        - end: time
    """
    end: time

    class Config:
        orm_mode=True


class SpecificGet(SpecificDaySID):
    """
    - day: date
    - start: time
    - prof_id: str
    - end: time
    - isCanceling: bool = False
    """
    end:time
    isCanceling: bool = False

    class Config:
        orm_mode= True

class SpecificUpdateInfo(BaseModel):
    """
    Esquema con la información para actualizar
        Nstart o Nend pueden no estar
        - day: date
        - start:time
        - Nstart: time
        - Nend: time
    """
    day: date
    start:time
    Nstart: Optional[time]
    Nend: Optional[time]

class SpecificUpdate(SpecificUpdateInfo, ProfessionalID):
    """
    Esquema que completa la información para actualizar
        - day: date
        - start:time
        - Nstart: time
        - Nend: time
        - prof_id: str
    """
    pass

class SpecificDayID(ProfessionalID):
    """
    - prof_id
    - day: date
    """
    day : date

### Topic Specific
#Esquema para pedir en insert
class TopicSpecificBase(BaseModel):
    """
    Esquema para agregar/eliminar un topico
        - day: date
        - start:time
        - topic_name: str
    """
    day: date
    start:time
    topic_name: str

#Esquema que se envia al crud
class TopicSpecificCreate(TopicSpecificBase, ProfessionalID):
    """
    Esquema que completa la informacion para agregar/eliminar un topico
        - day: date
        - start:time
        - topic_name: str
        - prof_id: str
    """

    class Config:
        orm_mode = True

#Respuesta get
class TopicSpecific(BaseModel):
    topic_name:str
    
    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True

class TopicSpecificSchema(ProfessionalID):
    """ 
        - day: date
        - start:time
        - prof_id: str
    """
    day: date
    start: time


class TopicSpecificCr1(BaseModel):
    """
    Esquema para la insercion de dias especificos con sus topicos
       - day: date
       - start: time
       - end: time
       - topics: list[Topic]
            - topic_name: str
    """
    day: date
    start: time
    end: time
    topics: list[Topic]

class TopicSpecificIn(TopicSpecificCr1, ProfessionalID):
    """
    Agrega los datos necesarios para la creacion
       - day: date
       - start: time
       - end: time
       - topics: list[Topic]
            - topic_name: str
       - prof_id: str
       - isCanceling: bool = False
    """
    isCanceling: bool = False


class TopicSpecificMonthYear(ProfessionalID):
    """
    Esquema que contine el prof_id y un month(int)
        Para recuperar los dias de un mes particular
            - prof_id: str
            - month: int
            - year: int = today().year
    """
    month: int
    year: int = date.today().year



