from app.models import Professional
from sqlalchemy.orm import Session
from .Repository import Repository

class ProfessionalRepository(Repository[Professional]):
    def __init__(self, session: Session):
        super().__init__(Professional, session)

    def create(self, data):
        return super().create(**data)