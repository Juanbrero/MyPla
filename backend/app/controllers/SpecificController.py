from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from ..bd.repositories.TopicSpecificRepository import TopicSpecificRepository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_specific
from ..services.specific_services.CreateSpecific import CreateSpecific
from ..services.specific_services.UpdateSpecific import UpdateSpecific
from ..services.specific_services.DeleteSpecific import DeleteSpecific
from ..services.specific_services.GetSpecifics import GetSpecifics

class SpecificController:
    def __init__ (self, db: Session):
        self.db = db
        self.specificR = SpecificScheduleRepository(db)
        self.meetingR = MeetingRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.topic_specificR = TopicSpecificRepository(db)
    
    def createSpecific (self, specificS: schema_topic_specific.TopicSpecificIn):
        return CreateSpecific.run(
            db = self.db, 
            specificS = specificS, 
            specificR = self.specificR, 
            professional_topicR = self.professional_topicR, 
            meetingR = self.meetingR,
            topic_specificR=self.topic_specificR
        )
    
    def getAllSpecifics (self, prof_id: str):
        return GetSpecifics.run(
            db = self.db,
            prof_id = prof_id,
            specificR = self.specificR
        )
    
    def updateSpecific (self, specificS: schema_topic_specific.TopicSpecificUpdate):
        return UpdateSpecific.run(
            db = self.db, 
            specificS = specificS, 
            specificR = self.specificR, 
            professional_topicR = self.professional_topicR, 
            meetingR = self.meetingR,
            topic_specificR=self.topic_specificR
        )
    
    def deleteSpecific (self, specificS: schema_topic_specific.TopicSpecificDeleteIn):
        return DeleteSpecific.run(
            db = self.db, 
            specificS = specificS, 
            specificR = self.specificR, 
            topic_specificR=self.topic_specificR
        )