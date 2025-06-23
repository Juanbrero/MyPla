from app.models import Class, Reservation, Meeting, Professional
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_, func, or_
from datetime import datetime

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
    
    def getCalificateProfessional(self, student_id:str):
        """
            Consulta que busca todas las clases PAGADAS o FINALIZADAS, que ya superaron su inicio y que aun no fueron calificadas
            - Recibe un student_id para buscar sus clases

        """
        stm = (
            select(Class)
            .join(Reservation, and_(
                Reservation.day_hour == Class.day_hour,
                Reservation.prof_id == Class.prof_id))
            .where(
                or_(
                    Reservation.state == 'pay', 
                    Reservation.state == 'finished'
                ),
                Reservation.student_id == student_id,
                func.now() >= Class.day_hour,
                Class.calificate_teacher.is_(None))
            )
        return self.session.execute(stm).scalars().all()
    
    def getCalificateStudent(self, prof_id:str):
        """
        Consulta que busca todas las clases PAGADAS o FINALIZADAS, que ya superaron su inicio y que aun no fueron calificadas
            - Recibe un pro_id para buscar sus clases
        """
        stm = (
            select(Class)
            .join(Reservation, and_(
                Reservation.day_hour == Class.day_hour,
                Reservation.prof_id == Class.prof_id
            ))
            .where(Class.calificate_student.is_(None),
                   func.now() >= Class.day_hour,
                   Class.prof_id == prof_id,
                   or_(
                    Reservation.state == 'pay', 
                    Reservation.state == 'finished'
                ))
        )
        return self.session.execute(stm).scalars().all()

    def getCalificationProfessional(self, prof_id: str):
        """
         Recupera las calificaciones de un profesional
             Args
                - prof_id
             Return
                - Calification( count, sum)
        
        """
        stm = (
            select(func.count(Class.calificate_teacher), func.sum(Class.calificate_teacher))
            .where(
                func.now() >= Class.day_hour,
                Class.prof_id == prof_id,
                Class.calificate_teacher.is_not(None)
            )
        )
        return self.session.execute(stm).first()
    
    def getClass(self, prof_id: str, day_hour:datetime, student_id:str):
        stm = (
            select(Class)
            .join(Reservation, and_(
                Reservation.student_id == student_id,
                Reservation.day_hour == day_hour,
                Reservation.prof_id == prof_id
            ))
            .where(
                or_(
                    Reservation.state == 'pay', 
                    Reservation.state == 'finished'
                ),
                Reservation.prof_id == prof_id,
                Reservation.day_hour == day_hour,
                Class.calificate_teacher.is_(None)
            )
        )
        return self.session.execute(stm).first()