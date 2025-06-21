from app.models import Reservation, Meeting, Professional, Student, Class, User
from backend.app.models import Event
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
    
    def getStudent(self, student_id:str):
        stm = (
            select(Reservation, Meeting.topic_name, User.username, Professional.link_class)
            .join(Meeting, and_(
                Meeting.prof_id == Reservation.prof_id,
                Meeting.day_hour == Reservation.day_hour
                )
            ).join(User,
                User.user_id == Reservation.prof_id
            )
            .join(Professional,
                  Professional.prof_id == Reservation.prof_id)
            .where(
                Reservation.student_id == student_id,
                Reservation.state == 'pay'
            ).order_by(Reservation.day_hour.asc())
        )
        return self.session.execute(stm)
    
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
      
    def getReservationForTransaction(self, reservation):
        stm = (
            select(Reservation)
            .where(
                Reservation.day_hour == reservation["day_hour"],
                Reservation.prof_id == reservation["prof_id"],
                Reservation.student_id == reservation["student_id"],
                Reservation.state.in_(["cancel_student", "cancel_professional", "pay"])
            )
        )
        return self.session.execute(stm).scalars().all()
