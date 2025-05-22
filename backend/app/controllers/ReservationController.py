from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ReservationRepository import ReservationRepository
from ..bd.repositories.ClassRepository import ClassRepository
from sqlalchemy.orm import Session
from ..services.reservation_services.CreateReservation import CreateReservation
from app.bd.schemas import schema_reservation 

class ReservationController:
    def __init__ (self, db: Session):
        self.db = db
        self.meetingR = MeetingRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.reservationR = ReservationRepository(db)
        self.classR = ClassRepository(db)
    
    def createReservation (self, reservationS: schema_reservation.ReservationClassIn):
        return CreateReservation.run(
            self.db, 
            self.reservationR,
            self.meetingR,
            self.professional_topicR,
            self.classR,
            reservationS
        )