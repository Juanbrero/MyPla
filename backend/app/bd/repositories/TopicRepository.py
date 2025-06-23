from app.models import Topic
from sqlalchemy.orm import Session
from sqlalchemy import select, text, cast, Time, func
from .Repository import Repository


class TopicRepository(Repository[Topic]):

    def __init__(self, session: Session):
        super().__init__(Topic, session)


    def create(self, topic_name: str):
        return super().create(**topic_name)
    
    def getCategory(self, category:str):
        stm = (
            select(Topic).where(Topic.category_name == category)
            )
        return self.session.execute(stm).scalars().all()