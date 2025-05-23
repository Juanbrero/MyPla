from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_specific
from ..services.specific_services.CreateSpecific import CreateSpecific

class SpecificController:
    def __init__ (self, db: Session):
        self.db = db
        self.specificR = SpecificScheduleRepository(db)
        self.meetingR = MeetingRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
    
    def createSpecific (self, specificS: schema_topic_specific.TopicSpecificIn):
        return CreateSpecific.run(
            db = self.db, 
            specificS = specificS, 
            specificR = self.specificR, 
            professional_topicR = self.professional_topicR, 
            meetingR = self.meetingR
        )