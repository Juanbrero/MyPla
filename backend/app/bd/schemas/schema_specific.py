from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class SpecificBase(BaseModel):
   
    start: time
    end: time

class SpecificCreate(SpecificBase):
    """
    Esquema que se esta utilizando en response como comodin hasta tener EVENT
        - start: time
        - end: time
        - day: date
        - isCanceling:bool
    """
    day: date
    isCanceling:bool

class Specific(SpecificBase):
    """
    Esquema que se esta utilizando en response como comodin hasta tener CLASE
        - day: date
        - start: time
        - end: time
    """
    day: date
    start: time
    end: time

    class Config:
        orm_mode=True


class SpecificSchema(Specific):
    """
        - prof_id: str 
        - day: date
        - start: time
        - end: time

    """
    prof_id: str



class ExceptionBase(BaseModel):
    """
    Esquema de datos que se deben recibir para crear una excepción
        - day: date
        - start: time
        - end: time
    """
    day:date
    start: time
    end: time

class ExceptionCreate(ExceptionBase):
    """
    Esquema que agrega el prof_id, para pasar a la funcion
        - day: date
        - start: time
        - end: time
        - prof_id: str
    """
    prof_id: str

class ExceptionInsert(ExceptionCreate):
    """
    Esquema que agrega el isCanceling True, para realizar la insercion
        - day: date
        - start: time
        - end: time
        - prof_id: str
        - isCanceling: bool = True
    """
    isCanceling: bool = True

class ExceptionGetDat(BaseModel):
    """
    Esquema que recibe el prof_id, y el dia a recuperar
        - prof_id: str
        - day: date
    """
    prof_id: str
    day: date

class ExceptionGet(ExceptionBase):


    class Config:
        orm_mode=True

class ExceptionDelDat(BaseModel):
    """
    Esquema con información necesaria para la eliminación
        - day: date
        - start: time
    """
    day: date
    start: time

class ExceptionDel(ExceptionDelDat):
    """
    Esquema que completa la información necesaria para eliminar una excepcion
        - day: date
        - start: time
        - prof_id: str
    """
    prof_id:str

class ExceptionUp(ExceptionDelDat):
    """
    Esquema que  recibe los datos para actualizar
        Se admite actualizar Nstart y/o Nend
        - day: date
        - start: time
        - Nstart: time puede no estar
        - Nend: time puede no estar
    """
    Nstart: Optional[time]
    Nend: Optional[time]

class ExceptionUpdate(ExceptionUp):
    """
    Esquema que  completa la información para actualizar
        - day: date
        - start: time
        - Nstart: time
        - Nend: time
        - prof_id: str

    """
    prof_id:str

