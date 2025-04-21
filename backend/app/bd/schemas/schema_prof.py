from pydantic import BaseModel
from typing import List



class ProfesionalBase(BaseModel):
    pass

class ProfesionalCreate(ProfesionalBase):
    pass


class Profesional(ProfesionalBase):
    user_id: int
    score: int

    class Config:
        orm_mode= True

