from app.models import Event
from sqlalchemy.orm import Session
from .Repository import Repository

class EventRepository(Repository[Event]):
    def __init__(self, session: Session):
        super().__init__(Event, session)

    def create(self, data):
        return super().create(**data)