from pydantic import BaseModel
from typing import List



class ProfessionalBase(BaseModel):
    pass

class ProfessionalCreate(ProfessionalBase):
    pass


class Professional(ProfessionalBase):
    prof_id: str
    score: float

    class Config:
        orm_mode= True

class ProfessionalID(ProfessionalBase):
    prof_id:str

class ProfessionalScore(ProfessionalBase):
    score:float