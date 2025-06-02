from app.models import Reservation, Meeting
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_, extract
from datetime import date

class ReservationRepository(Repository[Reservation]):
    def __init__(self, session: Session):
        super().__init__(Reservation, session)

    def create(self, data):
        return super().create(**data)
    

    def getReservationDayHour(self, prof_id:str, day: date):
        stm = (
            select(Reservation)
            .where(
                Reservation.prof_id == prof_id,
                extract('month', Reservation.day_hour) >= day.month,
                extract('month', Reservation.day_hour) <= day.month + 1,
                extract('year', Reservation.day_hour) == day.year,
                Reservation.cancel == False
            )
            .distinct().order_by(Reservation.day_hour.asc())
        )

        return self.session.execute(stm).scalars().all()