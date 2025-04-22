from pydantic import BaseModel


class ProfesionalTopicBase(BaseModel):
    topic_name: str
    user_id: int

class ProfesionalTopicCreate(ProfesionalTopicBase):
    pass

class ProfesionalTopic(BaseModel):
    topic_name: str
    
    class Config:
        orm_mode= True