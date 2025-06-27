from app.models import Cancelation
from sqlalchemy.orm import Session, aliased
from .Repository import Repository
from sqlalchemy import select, and_
from datetime import datetime
from app.models import User, Student, Professional

class CancelationRepository(Repository[Cancelation]):

    def __init__(self, db: Session):
        super().__init__(Cancelation, db)

    def create(self, data):
        return super().create(**data)
    
    def getCancelations(self):
        now = datetime.now()
    
        ProfUser = aliased(User)
        StudUser = aliased(User)
        stm = (
            select(
                Cancelation,
                Professional,
                Student,
                ProfUser.email.label("prof_email"),
                StudUser.email.label("stud_email")
            )
            .join(Professional, Cancelation.prof_id == Professional.prof_id)
            .join(Student, Cancelation.student_id == Student.student_id)
            .join(ProfUser, Professional.prof_id == ProfUser.user_id)
            .join(StudUser, Student.student_id == StudUser.user_id)
            .where(
                        Cancelation.refund == False
                    )
            ).order_by(Cancelation.cancel_time.asc())
        
        return self.session.execute(stm).all()