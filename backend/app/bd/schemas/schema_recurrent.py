from pydantic import BaseModel
from datetime import time
from .schema_prof import ProfessionalID

class RecurrentBase(BaseModel):
    """
    Esquema con los horarios de Recurrent
        - start: time
        - end: time
    """
    start: time
    end: time

class RecurrentCreate(RecurrentBase):
    """
    Esquema que complementa a RecurrentBase
        - start: time
        - end: time
        - week_day: int
    """
    week_day: int

class Recurrent(RecurrentBase):
    """
    Esquema de respuesta Recurrent

        - week_day: int
        - start: time
        - end: time
    """
    week_day: int
    start: time
    end: time

    class Config:
        orm_mode=True

class RecurrentDel(BaseModel):
    """
    Esqueam con la informacion para eliminar

        - week_day: int
        - start: time
    """
    week_day: int
    start: time

class RecurrentSchema(Recurrent, ProfessionalID):
    """
    Esquema que agrega al esquema de Recurrent el prof_id
        - week_day: int
        - start: time
        - end: time
        - prof_id: str
    """
    pass

