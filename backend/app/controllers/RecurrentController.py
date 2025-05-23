from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ReservationRepository import ReservationRepository
from ..bd.repositories.ClassRepository import ClassRepository
from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from sqlalchemy.orm import Session
from ..services.recurrent_services.CreateRecurrent import CreateRecurrent
from ..bd.schemas import schema_topic_recurrent

class RecurrentController:
    def __init__(self, db: Session):
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.recurrentR = RecurrentScheduleRepository,
        self.classR = ClassRepository(db)
        self.recurrentR = RecurrentScheduleRepository(db)
        self.specificR = SpecificScheduleRepository(db)

    
    def createRecurrent(self, recurrentS: schema_topic_recurrent.TopicRecurrentIn):
        return CreateRecurrent.run(
            db = self.db,
            recurrentR = self.recurrentR,
            meetingR = self.meetingR,
            professional_topicR = self.professional_topicR,
            classR = self.classR,
            recurrenS = recurrentS,
            specificR = self.specificR
        
        )