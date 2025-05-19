from .base import BaseRepository
from ..models import SpecificSchedule
from app.bd.schemas import schema_topic_specific
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, update



class SpecificRepository(BaseRepository[SpecificSchedule]):
    
    def __init__(self, db: Session):
        super().__init__(SpecificSchedule, db)

    def isCompleteHour(self, start, end):
        return super().isCompleteHour(start, end)
    
    def isValidTime(self, start, end):
        return super().isValidTime(start, end)
    
    def create(self, schedule:schema_topic_specific.SpecificSchema) -> SpecificSchedule:
        """
        Insert Specific Schedule
            Args:
                - schedule: dict
                    - day: date
                    - start: time
                    - end: time
                    - prof_id: str
            Return:
                - specific: SpecificSchedule
        """
        schedule.update({'isCanceling': False})
        specific = self.model(**schedule)
        return self.add(specific)
    
    def isInclude(self, schedule:schema_topic_specific.SpecificSchema):
        
        query = schedule.dict()
        query.pop('end')
        query.pop('start')
        query.update({'isCanceling':False})
        exist = self.filter_by(**query)
        return super().isInclude(exist, schedule.start, schedule.end)

    def get_day(self, specific_get: schema_topic_specific.SpecificDatID):
        """
        Get day complete
            Args:
                - specific_get: dict
                    - day: date (Completo)
                    - prof_id: str
                    - start: time
            Return:
                - response: SpecificSchedule
        """
        """query = {'isCanceling' : False,
        'day' : specific_get['day'],
        'prof_id' : specific_get['prof_id'],
        'start' : specific_get['start']}"""
        specific_get.update({'isCanceling': False})

        return self.first_by(**specific_get)

    def get_month_year(self, specific_get: schema_topic_specific.TopicSpecificMonthYear):
        """
        Recupera todos los dias de un mes año
            Args:
                -specific_get: dict
                    - prof_id: str
                    - month: int
                    - year: int = today().year

        """
        specific_get.update({'isCanceling': False})
        return self.filter_month_year(**specific_get)


    def update(self, specific: SpecificSchedule, specific_update:schema_topic_specific.SpecificSchema):
        """
        Actualiza hora de inicio y fin 
            Args:
                - specific: SpecificSchedule
                - specific_update: dict
                    - prof_id
                    - day
                    - start
                    - end
            Returns:
                - specific
        """
        specific.start = specific_update['start']
        specific.end = specific_update['end']
        self.commit()
        self.db.refresh(specific)
        return specific

    def delete(self, specific: SpecificSchedule):
        super().delete(specific)
        return 'OK'

    def commit(self):
        super().commit()
    
