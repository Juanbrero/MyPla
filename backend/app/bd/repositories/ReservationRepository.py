from app.models import Reservation, Meeting, Professional, Student, Events, Class, User
from sqlalchemy.orm import Session, aliased
from .Repository import Repository
from sqlalchemy import select, and_, extract, cast, or_, outerjoin
from datetime import date, datetime

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
    
    def getReservationsForTransaction(self):
        now = datetime.now()
    
        ProfUser = aliased(User)
        StudUser = aliased(User)
        stm = (
            select(
                Reservation,
                Professional,
                Student,
                ProfUser.email.label("prof_email"),
                StudUser.email.label("stud_email"),
                Class.price.label("price")
                #coalesce(Events.price, Class.price).label("price")
            )
            .join(Professional, Reservation.prof_id == Professional.prof_id)
            .join(Student, Reservation.student_id == Student.student_id)
            .join(ProfUser, Professional.prof_id == ProfUser.user_id)
            .join(StudUser, Student.student_id == StudUser.user_id)
            .join(Class, and_(
                Reservation.day_hour == Class.day_hour,
                Reservation.prof_id == Class.prof_id
            ))
            #.outerjoin(Events, Reservation.event_id == Events.id)
            #.outerjoin(Class, Reservation.class_id == Class.id)
            .where(
                or_(
                    and_(
                        Reservation.state == "pay",
                        Reservation.day_hour < now
                    ),
                    Reservation.state.in_(["cancel_student", "cancel_professional"])
                )
            )
        )
        return self.session.execute(stm).all()