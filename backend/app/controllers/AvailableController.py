from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.ExceptionScheduleRepository import ExceptionScheduleRepository
from ..bd.repositories.SpecificScheduleRepository import SpecificScheduleRepository
from ..bd.repositories.ClassRepository import ClassRepository

from ..services.available_services.GetProfessionalAvailable import GetProfessionalAvailable
from ..services.available_services.GetStudentAvailable import GetStudentAvailable

from sqlalchemy.orm import Session

from ..bd.schemas import schema_response


class AvailableController:
    
    def __init__(self, db: Session):
        self.db = db
        self.recurrentR = RecurrentScheduleRepository(db)
        self.exceptionR = ExceptionScheduleRepository(db)
        self.specificR = SpecificScheduleRepository(db)
        self.classR = ClassRepository(db)


    def getProfessionalAvailable(self, prof_id: str):
        return GetProfessionalAvailable.run(
            db = self.db,
            prof_id= prof_id,
            recurrentR= self.recurrentR,
            exceptionR= self.exceptionR,
            specificR= self.specificR,
            classR= self.classR
        )

    def getStudentAvailable(self, student_id: str):
        return GetStudentAvailable.run(
            db = self.db,
            student_id= student_id,
            recurrentR= self.recurrentR,
            exceptionR= self.exceptionR,
            specificR= self.specificR,
            classR= self.classR
        )