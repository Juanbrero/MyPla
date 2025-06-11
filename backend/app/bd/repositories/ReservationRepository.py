from app.models import Reservation, Meeting, User
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_, extract, cast, or_
from datetime import date

class ReservationRepository(Repository[Reservation]):
    def __init__(self, session: Session):
        super().__init__(Reservation, session)

    def create(self, data):
        return super().create(**data)
    

    def getReservationDayHour(self, prof_id:str, day: date, last_day:date):
        stm = (
            select(Reservation)
            .where(
                Reservation.prof_id == prof_id,
                 Reservation.day_hour >= day,
                 Reservation.day_hour <= last_day,
                Reservation.cancel == False
            )
            .distinct().order_by(Reservation.day_hour.asc())
        )
        return self.session.execute(stm).scalars().all()
    
    def getStudent(self, student_id:str):
        stm = (
            select(Reservation, Meeting.topic_name, User.username)
            .join(Meeting, and_(
                Meeting.prof_id == Reservation.prof_id,
                Meeting.day_hour == Reservation.day_hour
                )
            ).join(
                User.user_id == Reservation.prof_id
            )
            .where(
                Reservation.student_id == student_id,
                Reservation.state == 'pay'
            ).order_by(Reservation.day_hour.asc())
        )
        return self.session.execute(stm)