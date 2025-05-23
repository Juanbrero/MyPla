from app.models import ProfessionalTopic
from sqlalchemy.orm import Session
from .Repository import Repository

class ProfessionalTopicRepository(Repository[ProfessionalTopic]):
    def __init__(self, session: Session):
        super().__init__(ProfessionalTopic, session)
    
    def create(self, data):
        return super().create(**data)