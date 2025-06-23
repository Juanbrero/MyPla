from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ReservationRepository import ReservationRepository
from ..bd.repositories.TopicSpecificRepository import TopicSpecificRepository
from ..bd.repositories.ClassRepository import ClassRepository
from ..bd.repositories.CancelationRepository import CancelationRepository
from sqlalchemy.orm import Session
from ..services.pay_services.PayInitialService import PayInitialService
from ..services.pay_services.CreatePreference import CreatePreference
from ..services.pay_services.GetPayPending import GetPayPending
from ..services.pay_services.ModifyPayPending import ModifyPayPending

class PayController:
    def __init__ (self, db: Session):
        self.db = db
        self.reservationR = ReservationRepository(db)
        self.meetingR = MeetingRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.topic_specificR = TopicSpecificRepository(db)
        self.classR = ClassRepository(db)
        self.cancelationR = CancelationRepository(db)
    
    def initialPay (self, student_id: str, method: str):
        return PayInitialService.run(
            db = self.db, 
            reservationR = self.reservationR,
            meetingR = self.meetingR,
            classR = self.classR,
            student_id = student_id
        )

    def createPreference(self,student_id:str):
        return CreatePreference.run(
            reservationR = self.reservationR,
            classR = self.classR,
            student_id = student_id
        )
    
    def getPayPending (self):
        return GetPayPending.run(
            reservationR = self.reservationR,
            cancelationR = self.cancelationR
        )
    
    def modifyPayPending (self, reservationS: str):
        return ModifyPayPending.run(
            db=self.db,
            reservationR = self.reservationR,
            reservationS = reservationS,
            cancelationR = self.cancelationR
        )