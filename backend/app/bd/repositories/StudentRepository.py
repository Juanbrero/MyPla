from app.models import Student
from sqlalchemy.orm import Session
from .Repository import Repository

class StudentRepository(Repository[Student]):
    def __init__(self, session: Session):
        super().__init__(Student, session)

    def create(self, data):
        return super().create(**data)