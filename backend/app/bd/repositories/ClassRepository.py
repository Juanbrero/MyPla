from app.models import Class
from sqlalchemy.orm import Session
from .Repository import Repository

class ClassRepository(Repository[Class]):
    def __init__(self, session: Session):
        super().__init__(Class, session)
    
    def create(self, data):
        return super().create(**data)