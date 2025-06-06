from app.models import Professional, User

from sqlalchemy.orm import Session
from sqlalchemy import select
from .Repository import Repository

class ProfessionalRepository(Repository[Professional]):
    def __init__(self, session: Session):
        super().__init__(Professional, session)

    def create(self, data):
        return super().create(**data)
    
    def getInfo(self, prof_id:str):
        stm=(
            select(User, Professional.score).join(
                Professional, Professional.prof_id == User.user_id)
        ).where(
                User.user_id == prof_id
            ).order_by(
                Professional.prof_id.asc())
        return self.session.execute(stm).first()