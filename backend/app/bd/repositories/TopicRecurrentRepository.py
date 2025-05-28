from app.models import TopicRecurrent
from sqlalchemy.orm import Session, selectinload
from .Repository import Repository
from sqlalchemy import select, cast, Time, func
from datetime import datetime

class TopicRecurrentRepository(Repository[TopicRecurrent]):

    def __init__(self, session: Session):
        super().__init__(TopicRecurrent, session)

    def create(self, data):
        return super().create(**data)
    

    