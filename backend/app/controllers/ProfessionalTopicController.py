
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.TopicRepository import TopicRepository
from ..bd.repositories.ProfessionalRepository import ProfessionalRepository
from ..bd.repositories.TopicRecurrentRepository import TopicRecurrentRepository
from ..bd.repositories.TopicSpecificRepository import TopicSpecificRepository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_prof_topic
from app.services.professional_topic_services.CreateProfTopic import CreateProfTopic
from app.services.professional_topic_services.GetProfTopic import GetProfTopic
from app.services.professional_topic_services.UpdatePrice import UpdatePrice
from app.services.professional_topic_services.DelProfTopic import DelProfTopic
from app.services.professional_topic_services.GetTopicProf import GetTopicProf


class ProfessionalTopicController:

    def __init__(self, db:Session):
        self.db = db
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.topicR = TopicRepository(db)
        self.professioanlR = ProfessionalRepository(db)
        self.topic_recurrentR = TopicRecurrentRepository(db)
        self.topic_specificR = TopicSpecificRepository(db)

    def createProfTopic(self, prof_topicS:schema_prof_topic.ProfessionalTopic):
        return CreateProfTopic.run(
            db= self.db,
            prof_topicS = prof_topicS,
            professional_topicR= self.professional_topicR,
            topicR= self.topicR
        )
    
    def getProfTopic(self, prof_id: str):
        return GetProfTopic.run(
            db = self.db,
            prof_id= prof_id,
            professional_topicR= self.professional_topicR
        )

    def updatePrice(self, prof_topicS:schema_prof_topic.ProfessionalTopic):
        return UpdatePrice.run(
            db= self.db,
            prof_topicS = prof_topicS,
            professional_topicR= self.professional_topicR
        )
    
    def deleteProfTopic(self, prof_topicS:schema_prof_topic.ProfessionalTopicDel):
        return DelProfTopic.run(
            db= self.db,
            prof_topicS = prof_topicS,
            professional_topicR= self.professional_topicR,
            topic_recurrentR = self.topic_recurrentR,
            topic_specificR= self.topic_specificR
        )
    
    def getTopicProf(self, topic_name: str):
        return GetTopicProf.run(
            db = self.db,
            topic_name= topic_name,
            professional_topicR= self.professional_topicR,
            professionalR= self.professioanlR
            
        )