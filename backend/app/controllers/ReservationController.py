from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ReservationRepository import ReservationRepository
from ..bd.repositories.ClassRepository import ClassRepository
from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from sqlalchemy.orm import Session
from ..services.reservation_services.CreateReservation import CreateReservation
from ..services.reservation_services.UpdatePay import UpdatePay
from ..services.reservation_services.CancelReservation import CancelReservation
from app.bd.schemas import schema_reservation 
from datetime import datetime
from app.services.reservation_services.StudentReservation import StudentReservation

class ReservationController:
    def __init__ (self, db: Session):
        self.db = db
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
    
    def updatePay(self, student_id:str, statusP: str):
        return UpdatePay.run(
            db= self.db,
            student_id = student_id,
            statusP= statusP,
            reservationR = self.reservationR,
            meetingR= self.meetingR
        )
    
    def cancelReservation(self, day_hour:datetime, user_id:str, user_cancel:str, role:str):
        return CancelReservation.run(
            db = self.db,
            day_hour = day_hour,
            user_id = user_id,
            user_cancel = user_cancel,
            role = role,
            reservationR = self.reservationR
        )
    def studentReservation(self, student_id:str):
        return StudentReservation.run(
            student_id = student_id,
            reservationR = self.reservationR
        )
    
