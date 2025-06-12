from app.models import Class, Reservation, Meeting
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_, cast, Date
from datetime import date

class ClassRepository(Repository[Class]):
    def __init__(self, session: Session):
        super().__init__(Class, session)
    
    def create(self, data):
        return super().create(**data)
    

    def getTopicClass(self, prof_id:str, day:date, last_day:date):
        smt= (
            select(Class, Reservation.student_id, Meeting.topic_name)
            .join(Meeting, and_(
                   Class.prof_id == Meeting.prof_id,
                   Class.day_hour == Meeting.day_hour))
            .join(Reservation, and_(
                Class.day_hour == Reservation.day_hour,
                Class.prof_id == Reservation.prof_id
            ))
            .where(Class.prof_id == prof_id, 
                   Reservation.state == 'pay',
                   cast(Reservation.day_hour, Date) >= day,
                   cast(Reservation.day_hour, Date) <= last_day)
            .order_by(Class.day_hour.asc())
        )
        return self.session.execute(smt)