from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.TopicRecurrentRepository import TopicRecurrentRepository
from sqlalchemy.orm import Session

from ..services.topic_recurrent_services.AddTopicRecurrent import AddTopicRecurrent
from ..services.topic_recurrent_services.DelTopicRecurrent import DelTopicRecurrent

from ..bd.schemas import schema_topic_recurrent

class TopicRecurrentController:
    def __init__(self, db: Session):
        self.db = db
        self.recurrentR = RecurrentScheduleRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.topic_recurrentR = TopicRecurrentRepository(db)

    def addTopic(self, topic_recurrentS:schema_topic_recurrent.TopicRecurrentIn):
        return AddTopicRecurrent.run(
            db = self.db,
            topic_recurrentS = topic_recurrentS,
            recurrentR = self.recurrentR,
            professional_topicR = self.professional_topicR,
            topic_recurrentR = self.topic_recurrentR 
        )
    
    def delTopic(self, topic_recurrentS:schema_topic_recurrent.TopicRecurrentIn):
        return DelTopicRecurrent.run(
            db = self.db,
            topic_recurrentS = topic_recurrentS,
            recurrentR = self.recurrentR,
            professional_topicR = self.professional_topicR,
            topic_recurrentR = self.topic_recurrentR 
        )