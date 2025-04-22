from pydantic import BaseModel


class ProfesionalTopicBase(BaseModel):
    topic_name: str
    user_id: int

class ProfesionalTopicCreate(ProfesionalTopicBase):
    pass

class ProfesionalTopic(ProfesionalTopicBase):
    topic_name: str
    user_id: int
    
    class Config:
        orm_mode= True