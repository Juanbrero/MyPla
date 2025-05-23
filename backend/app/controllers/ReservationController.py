from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ReservationRepository import ReservationRepository
from ..bd.repositories.ClassRepository import ClassRepository
from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from sqlalchemy.orm import Session
from ..services.reservation_services.CreateReservation import CreateReservation
from app.bd.schemas import schema_reservation 

class ReservationController:
    def __init__ (self, db: Session):
        self.meetingR = MeetingRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.reservationR = ReservationRepository(db)
        self.classR = ClassRepository(db)
        self.recurrentR = RecurrentScheduleRepository(db)
        self.specificR = SpecificScheduleRepository(db)
    
    def createReservation (self, reservationS: schema_reservation.ReservationClassIn):
        return CreateReservation.run(
            db = self.db, 
            reservationR = self.reservationR,
            meetingR = self.meetingR,
            professional_topicR = self.professional_topicR,
            recurrentR = self.recurrentR,
            classR = self.classR,
            reservationS = reservationS,
            specificR = self.specificR
        )