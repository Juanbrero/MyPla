from pydantic import BaseModel
from datetime import time

class RecurrentBase(BaseModel):
    start: time
    end: time

class RecurrentCreate(RecurrentBase):
    name_day: str

class Recurrent(RecurrentBase):
    name_day: str
    start: time
    end: time

    class Config:
        orm_mode=True