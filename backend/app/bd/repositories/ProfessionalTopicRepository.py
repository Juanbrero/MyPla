from app.models import ProfessionalTopic
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, func

class ProfessionalTopicRepository(Repository[ProfessionalTopic]):
    def __init__(self, session: Session):
        super().__init__(ProfessionalTopic, session)
    
    def create(self, data):
        return super().create(**data)
    
    def checkTopicProf(self, prof_id: str, topic_names: list[str]) -> bool:
        stmt = (
            select(func.count())
            .select_from(ProfessionalTopic)
            .where(
                ProfessionalTopic.prof_id == prof_id,
                ProfessionalTopic.topic_name.in_(topic_names)
            )
        )
        result = self.session.execute(stmt).scalar_one()
        return result == len(topic_names)
    

    def getTopics(self, prof_id: str):
        """
        Recupera todos los topicos de un professional
        """
        stm = (
            select(ProfessionalTopic.topic_name)
            .where(ProfessionalTopic.prof_id == prof_id)
        )
        result = self.session.execute(stm).scalars().all()
        return result