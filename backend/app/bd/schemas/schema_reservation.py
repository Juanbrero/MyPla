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

class reservstudent(BaseModel):
    prof_username: str
    prof_id: str
    day_hour: datetime
    topic:str
    link_class: str

class StudentReservation(BaseModel):
    reservations: list[reservstudent]
