from pydantic import BaseModel
from datetime import date, time, datetime
from typing import List

class EventBase(BaseModel):
    day_hour: datetime
    duration: int
    price: float
    invites: List[str]
    topic: str
    
class EventGet(BaseModel):
    page: int
    amount: int