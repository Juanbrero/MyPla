from pydantic import BaseModel
from .schema_prof import ProfessionalID


class ProfessionalTopicBase(BaseModel):
    """
    Esquema de petición de la relación profesional topico
        - topic_name: str
        - price_class: float
    """
    topic_name: str
    price_class: float

class ProfessionalTopicCreate(ProfessionalTopicBase):
    """
        - topic_name: str
        - price_class: float
    """
    pass

class ProfessionalTopic(BaseModel):
    """
    Esquema con toda la información perteneciente a la relación profesional topico
        - topic_name: str
        - prof_id:str
        - price_class: float
    """
    topic_name: str
    prof_id:str
    price_class: float
    
    class Config:
        orm_mode= True

class ProfessionalTopicsList(BaseModel):
    """
    Esquema para almacenar y retornar una lista de topicos
        - topic_name: list[str]
    """
    topic_name: list[str]

class ProfessionalTopicDel(ProfessionalID):
    """
    Esquema utilzado para la eliminación,
        - prof_id: str
        - topic_name: str
    """
    topic_name: str