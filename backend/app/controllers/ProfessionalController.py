from ..bd.repositories.ProfessionalRepository import ProfessionalRepository
from sqlalchemy.orm import Session
from app.services.professional_services.GetProfessional import GetProfessional

class ProfessionalController:

    def __init__(self, db:Session):
        self.db = db
        self.professioanlR = ProfessionalRepository(db)

    def getProfessional(self, prof_id:str):
        return GetProfessional.run(
            db = self.db,
            prof_id = prof_id,
            professionalR = self.professioanlR
        )