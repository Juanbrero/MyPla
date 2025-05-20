from .schedule_repository import ScheduleRepository
from ..models import SpecificSchedule
from app.bd.schemas import schema_topic_specific
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, update
from datetime import time


class SpecificRepository(ScheduleRepository[SpecificSchedule]):
    
    def __init__(self, db: Session):
        super().__init__(SpecificSchedule, db)

    def trunc_time(self, horario):
        """
        Trunca el horario a horas y minutos
        """
        return super().trunc_time(horario)

    def isCompleteHour(self, start:time, end:time):
        return super().isCompleteHour(start, end)
    
    def isValidTime(self, start:time, end:time):
        return super().isValidTime(start, end)
    
    def isInclude(self, schedule:schema_topic_specific.SpecificSchema):
        """
            Args:
               - schedule:dict
                    - prof_id
                    - start
                    - end
                    - day
            Return
                - True Esta incluido
                - False No esta Incluido
        """
        query = schedule.copy()
        query.pop('end')
        query.pop('start')
        query.update({'isCanceling':False})
        exist = self.filter_by(**query)
        return super().isInclude(exist, schedule['start'], schedule['end'])    
    
    def isIncludeUpdate(self, start:time, schedule:schema_topic_specific.SpecificSchema):
        """
        Busca si el valor ingresado esta en la DB, omitiendo el valor start (valor a actualizar)
        """
        query = schedule.copy()
        query.pop('end')
        query.pop('start')
        query.update({'isCanceling': False})
        exist = self.get_ommit(start,**query)
        return super().isInclude(exist, schedule['start'], schedule['end'])

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
            Returns:
                - List[SpecificSchedule]

        """
        specific_get.update({'isCanceling': False})
        return self.filter_month_year(**specific_get)


    def update(self, specific: SpecificSchedule, specific_update:schema_topic_specific.SpecificSchema):
        """
        Actualiza hora de inicio y fin 
            Args:
                - specific: OBJ: SpecificSchedule
                - specific_update: dict
                    - prof_id
                    - day
                    - start
                    - end
            Returns:
                - specific
        """
        return super().update(specific, specific_update)

    def delete(self, specific: SpecificSchedule):
        """
        - specific: OBJ: SpecificSchedule
        """
        super().delete(specific)
        return True

    def commit(self):
        super().commit()
    
