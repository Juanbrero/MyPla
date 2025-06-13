from datetime import datetime
from pydantic import BaseModel


class ReservationClassCtrl(BaseModel):
    day_hour: datetime
    prof_id: str
    topic: str

class ReservationClassIn(ReservationClassCtrl):
    student_id: str
    
class PayPending(BaseModel):
    day_hour: datetime
    prof_id: str
    student_id: str
