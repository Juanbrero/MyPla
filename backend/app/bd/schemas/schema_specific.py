from pydantic import BaseModel
from datetime import date, time

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