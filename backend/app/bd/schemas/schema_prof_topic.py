from pydantic import BaseModel


class ProfessionalTopicBase(BaseModel):
    topic_name: str
    price_class:float

class ProfessionalTopicCreate(ProfessionalTopicBase):
    pass

class ProfessionalTopic(BaseModel):
    topic_name: str
    prof_id:str
    price_class: float
    
    class Config:
        orm_mode= True

class ProfessionalTopicsList(BaseModel):
    topic_name: list[str]

class ProfessionalTopicID(BaseModel):
    prof_id:str

class ProfessionalTopicDel(ProfessionalTopicID):
    topic_name:str