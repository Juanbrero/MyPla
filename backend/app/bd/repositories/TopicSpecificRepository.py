from app.models import TopicSpecific
from sqlalchemy.orm import Session
from .Repository import Repository

class TopicSpecificRepository(Repository[TopicSpecific]):
    def __init__(self, session: Session):
        super().__init__(TopicSpecific, session)

    def create(self, data):
        return super().create(**data)