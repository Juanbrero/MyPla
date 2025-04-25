from pydantic import BaseModel
from datetime import date, time

class SpecificBase(BaseModel):
    start: time
    end: time

class SpecificCreate(SpecificBase):
    day: date
    pass

class Specific(SpecificBase):
    day: date
    start: time
    end: time

    class Config:
        orm_mode=True

class SpecificIsCancel(BaseModel):
    isCanceling: bool

    class Config:
        orm_mode=True