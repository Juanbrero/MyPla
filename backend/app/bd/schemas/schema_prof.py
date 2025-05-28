from pydantic import BaseModel
from typing import List



class ProfessionalBase(BaseModel):
    pass

class ProfessionalCreate(ProfessionalBase):
    pass


class Professional(ProfessionalBase):
    """
    Esquema completo para retorno de Profesional
        - prof_id: str
        - score: float
    """
    prof_id: str
    score: float

    class Config:
        orm_mode= True

class ProfessionalID(ProfessionalBase):
    """
    Esquema de prof_id
        - prof_id: str
    """
    prof_id:str

class ProfessionalScore(ProfessionalBase):
    """
    Esquema de score   
        - score: float
    """
    score:float