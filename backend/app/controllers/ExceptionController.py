from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.ExceptionScheduleRepository import ExceptionScheduleRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from ..services.exception_services.CreateException import CreateException
from ..services.exception_services.GetExceptions import GetExceptions
from ..services.exception_services.UpdateException import UpdateExceptions
from ..services.exception_services.DeleteException import DeleteException
from sqlalchemy.orm import Session
from app.bd.schemas import schema_exception


class ExceptionController():

    def __init__ (self, db: Session):
        self.db = db
        self.exceptionR = ExceptionScheduleRepository(db)
        self.meetingR = MeetingRepository(db)


    def createException(self, exceptionS: schema_exception.ExceptionCreate):
        return CreateException.run(
            db = self.db, 
            exceptionS = exceptionS, 
            exceptionR = self.exceptionR, 
            meetingR = self.meetingR
        )
    
    def getException(self, prof_id: str):
        return GetExceptions.run(
            db = self.db, 
            prof_id = prof_id, 
            exceptionR = self.exceptionR
        )

    def updateException(self, exceptionS: schema_exception.ExceptionUpdate):
        return UpdateExceptions.run(
            db = self.db, 
            exceptionS = exceptionS, 
            exceptionR = self.exceptionR, 
            meetingR = self.meetingR
        )

    def deleteException(self, exceptionS: schema_exception.ExceptionDelete):
        return DeleteException.run(
            db = self.db, 
            exceptionS = exceptionS, 
            exceptionR = self.exceptionR
        )
    