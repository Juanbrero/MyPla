from ..bd.repositories.ProfessionalTopicRepository import ProfessionalTopicRepository
from ..bd.repositories.RecurrentScheduleRepository import RecurrentScheduleRepository
from ..bd.repositories.TopicRecurrentRepository import TopicRecurrentRepository
from sqlalchemy.orm import Session

from ..services.recurrent_services.CreateRecurrent import CreateRecurrent
from ..services.recurrent_services.GetRecurrentWeek import GetRecurrentWeek
from ..services.recurrent_services.DelRecurrent import DelRecurrent
from ..services.recurrent_services.UpRecurrent import UpRecurrent

from ..bd.schemas import schema_topic_recurrent

class RecurrentController:
    def __init__(self, db: Session):
        self.db = db
        self.recurrentR = RecurrentScheduleRepository(db)
        self.professional_topicR = ProfessionalTopicRepository(db)
        self.topic_recurrentR = TopicRecurrentRepository(db)
    
    def createRecurrent(self, recurrentS: schema_topic_recurrent.TopicRecurrentIn):
        return CreateRecurrent.run(
            db = self.db,
            recurrentS = recurrentS,
            recurrentR = self.recurrentR,
            professional_topicR = self.professional_topicR,
            topic_recurrentR = self.topic_recurrentR        
        )
    
    def getRecurrentWeek(self, recurrentS: schema_topic_recurrent.TopicRecurrentWeekGet):
        """
        Recupera los dias de la semana y hora de un professional, con sus topicos
        en un dia de la semana solicitado
        """
        return GetRecurrentWeek.run(
            db = self.db,
            recurrentS = recurrentS,
            recurrentR = self.recurrentR
        )
    
    def delRecurrent(self, recurrentS: schema_topic_recurrent.TopicRecurrentSchema):
        return DelRecurrent.run(
            db = self.db,
            recurrentS = recurrentS,
            recurrentR = self.recurrentR
        )
    
    def updateRecurrent(self, recurrentS: schema_topic_recurrent.TopicRecurrentUpdate):
        return UpRecurrent.run(
            db = self.db,
            recurrentS = recurrentS,
            recurrentR = self.recurrentR
        )