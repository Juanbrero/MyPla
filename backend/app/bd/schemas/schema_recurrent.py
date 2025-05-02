from pydantic import BaseModel
from datetime import time

class RecurrentBase(BaseModel):
    start: time
    end: time

class RecurrentCreate(RecurrentBase):
    week_day: int

class Recurrent(RecurrentBase):
    week_day: int
    start: time
    end: time

    class Config:
        orm_mode=True

class RecurrentDel(BaseModel):
    week_day: int
    start: time

class RecurrentSchema(Recurrent):
    prof_id:str

class RecurrentSchemaID(BaseModel):
    prof_id:str
