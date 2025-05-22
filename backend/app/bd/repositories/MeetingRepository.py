from app.models import Meeting
from sqlalchemy.orm import Session
from .Repository import Repository

class MeetingRepository(Repository[Meeting]):
    def __init__(self, session: Session):
        super().__init__(Meeting, session)
    
    #def create(self, data):
    #    return super().create(**data)