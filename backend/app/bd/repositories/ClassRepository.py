from app.models import Class, Reservation, Meeting, Professional
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_


class ClassRepository(Repository[Class]):
    def __init__(self, session: Session):
        super().__init__(Class, session)
    
    def create(self, data):
        return super().create(**data)
    

    def getTopicClass(self, prof_id:str):
        smt= (
            select(Class, Reservation.student_id, Meeting.topic_name, Professional.link_class)
            .join(Meeting, and_(
                   Class.prof_id == Meeting.prof_id,
                   Class.day_hour == Meeting.day_hour))
            .join(Reservation, and_(
                Class.day_hour == Reservation.day_hour,
                Class.prof_id == Reservation.prof_id
            ))
            .join(Professional, 
                  Professional.prof_id == Class.prof_id)
            .where(Class.prof_id == prof_id,
                   Reservation.state == "pay")
        )
        return self.session.execute(smt)