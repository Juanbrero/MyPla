from sqlalchemy.orm import Session
from app.bd.repositories.ClassRepository import ClassRepository
from app.bd.repositories.ProfessionalRepository import ProfessionalRepository
from app.bd.repositories.StudentRepository import StudentRepository

from app.services.calificate_services.GetCalifications import GetCalification
from app.services.calificate_services.CalificateProfessional import CalificateProfessional


from datetime import datetime

class CalificationController():
    def __init__(self, db: Session):
        self.db = db
        self.classR = ClassRepository(db)
        self.professionalR = ProfessionalRepository(db)

    
    def getCalificate(self, id:str, role:str):
        return GetCalification.run(db= self.db,
                                    id= id,
                                    role= role,
                                   classR= self.classR)
    
    def calificateProfessional(self, student_id:str, day_hour:datetime, prof_id:str, score:int):
        return CalificateProfessional.run(db= self.db,
                                        classR = self.classR,
                                        professionalR= self.professionalR,
                                        student_id = student_id,
                                        prof_id = prof_id,
                                        day_hour= day_hour,
                                        score = score)
    
