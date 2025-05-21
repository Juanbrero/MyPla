from .schedule_repository import ScheduleRepository
from ..models import RecurrentSchedule
from app.bd.schemas import schema_topic_recurrent
from sqlalchemy.orm import Session
from sqlalchemy import func, update
from datetime import time



class RecurrentRepository(ScheduleRepository[RecurrentSchedule]):

    def __init__(self, db: Session):
        super().__init__(RecurrentSchedule, db)

    
    def trunc_time(self, horario):
        """
        Trunca el horario a horas y minutos
        """
        return super().trunc_time(horario)

    def isCompleteHour(self, start:time, end:time):
        return super().isCompleteHour(start, end)
    
    def isValidTime(self, start:time, end:time):
        return super().isValidTime(start, end)
    
    def isInclude(self, schedule: schema_topic_recurrent.RecurrentSchema):
        """
            Args:
               - schedule: RecurrentSchema
                    - prof_id
                    - start
                    - end
                    - week_day
            Return
                - True Esta incluido
                - False No esta Incluido
        """
        query = schedule.dict()
        query.pop('end')
        query.pop('start')
        exist = self.filter_by(**query)
        return super().isInclude(exist, schedule.start, schedule.end)    
    
    def isIncludeUpdate(self, start:time, schedule: schema_topic_recurrent.RecurrentSchema):
        """
        Busca si el valor ingresado esta en la DB, omitiendo el valor start (valor a actualizar)
        """
        query = schedule.dict()
        query.pop('end')
        query.pop('start')
        exist = self.get_ommit(start, **query)
        return super().isInclude(exist, schedule.start, schedule.end)

    def create(self, schedule:schema_topic_recurrent.RecurrentSchema) -> RecurrentSchedule:
        """
        Insert Specific Schedule
            Args:
                - schedule: RecurrentSchema
                    - week_day: int
                    - start: time
                    - end: time
                    - prof_id: str
            Return:
                - recurrent: RecurrentSchedule
        """
        recurrent = self.model(**schedule.dict())
        return self.add(recurrent)
    
    def filter_month_year(self):
        return NotImplemented

    def get_recurrent(self, prof_id: schema_topic_recurrent.ProfessionalID):
        """
        Recupera todos los dias
            Args:
                - prof_id: str
            Returns:
                - List[RecurrentSchedule] | []

        """
        return self.filter_by(**prof_id.dict())

    def get_recurrent_week(self, recurrent:schema_topic_recurrent.RecurrentWID):
        """
        Recupera todos los horarios de un dia de semana particular
            Return
                - List[RecurrentSchedule] | []
        """
        recurrent_get = recurrent.dict()
        return self.filter_by(**recurrent_get)
    
    def get_recurrent_week_start(self, recurrent:schema_topic_recurrent.RecurrentGet):
        """
        Recupera un dia de la semana en un horario particular
            Return
                - RecurrentSchedule | None
        """
        recurrent_get = recurrent.dict()
        return self.first_by(**recurrent_get)

    def update(self, recurrent: RecurrentSchedule, recurrent_update:schema_topic_recurrent.RecurrentSchema):
        """
        Actualiza hora de inicio y fin 
            Args:
                - recurrent: OBJ: RecurrentSchedule
                - recurrent_update: RecurrentSchema
                    - prof_id
                    - week
                    - start
                    - end
            Returns:
                - recurrent
        """
        return super().update(recurrent, recurrent_update)

    def delete(self, recurrent: RecurrentSchedule):
        """
        - recurrent: OBJ: RecurrentSchedule
        """
        super().delete(recurrent)
        return True

    def commit(self):
        super().commit()