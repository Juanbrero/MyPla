from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class SpecificBase(BaseModel):
    start: time
    end: time

class SpecificCreate(SpecificBase):
    day: date
    isCanceling:bool

class Specific(SpecificBase):
    day: date
    start: time
    end: time

    class Config:
        orm_mode=True

class SpecificID(BaseModel):
    prof_id:str


class SpecificDel(BaseModel):
    day: date
    start: time

class SpecificSchema(Specific):
    prof_id: str

class SpecificIsCancel(SpecificSchema):
    isCanceling: bool

    class Config:
        orm_mode=True

class SpecificSchemaID(BaseModel):
    prof_id:str




class ExceptionBase(BaseModel):
    day:date
    start: Optional[time]
    end: Optional[time]

class ExceptionCreate(ExceptionBase):
    prof_id: str

class ExceptionInsert(ExceptionCreate):
    isCanceling: bool = True

class ExceptionGetDat(BaseModel):
    prof_id:str
    day:date

class ExceptionGet(ExceptionBase):

    class Config:
        orm_mode=True

class ExceptionDelDat(BaseModel):
    day: date
    start: time

class ExceptionDel(ExceptionDelDat):
    prof_id:str

class ExceptionUp(ExceptionDelDat):
    Nstart: Optional[time]
    Nend: Optional[time]

class ExceptionUpdate(ExceptionUp):
    prof_id:str

