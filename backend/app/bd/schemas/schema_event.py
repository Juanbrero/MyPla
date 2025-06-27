from pydantic import BaseModel
from datetime import date, time, datetime
from typing import List

class EventBase(BaseModel):
    day_hour: datetime
    duration: int
    price: float
    invites: List[str]
    topic: str
    title: str
    
class EventGet(BaseModel):
    page: int
    amount: int
    
class InviteConfirm(BaseModel):
    prof_id: str
    day_hour: datetime
    accept: bool