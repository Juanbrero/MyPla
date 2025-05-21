from .schedule_repository import ScheduleRepository
from ..models import SpecificSchedule
from app.bd.schemas import schema_exception
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, update
from datetime import time


class ExceptionRepository(ScheduleRepository[SpecificSchedule]):
    
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
    
    def isInclude(self, schedule: schema_exception.ExceptionCreate):
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
        query = schedule.dict()
        query.pop('end')
        query.pop('start')
        query.update({'isCanceling':True})
        exist = self.filter_by(**query)
        return super().isInclude(exist, schedule.start, schedule.end)    
    
    def isIncludeUpdate(self, start:time, schedule: schema_exception.ExceptionCreate):
        """
        Busca si el valor ingresado esta en la DB, omitiendo el valor start (valor a actualizar)
        """
        query = schedule.dict()
        query.pop('end')
        query.pop('start')
        query.update({'isCanceling': True})
        exist = self.get_ommit(start, **query)
        return super().isInclude(exist, schedule.start, schedule.end)

    def create(self, schedule:schema_exception.ExceptionCreate) -> SpecificSchedule:
        """
        Insert Specific Schedule
            Args:
                - schedule: ExceptionCreate
                    - day: date
                    - start: time
                    - end: time
                    - prof_id: str
            Return:
                - excepcion: SpecificSchedule
        """
        schedule_dict = schedule.dict()
        schedule_dict.update({'isCanceling': True})
        excepcion = self.model(**schedule_dict)
        return self.add(excepcion)
    
    def get_day_hours(self, excepcion_get:schema_exception.ExceptionGetDat):
        """
        Recupera todos los horarios de un dia
            - prof_id
            - day
        """
        excepcion_dict = excepcion_get.dict()
        excepcion_dict.update({'isCanceling': True})
        return self.filter_by(**excepcion_dict)
        

    def get_day(self, excepcion_get:schema_exception.ExceptionDel):
        """
        Get day 
            Args:
                - excepcion_get: Exception
                    - day: date (Completo)
                    - prof_id: str
            Return:
                - response: SpecificSchedule
        """
        excepcion_dict = excepcion_get.dict()
        excepcion_dict.update({'isCanceling': True})
             
        return self.first_by(**excepcion_dict)

    def get_month_year(self, excepcion_get:schema_exception.ExceptionMonthYear):
        """
        Recupera todos los dias de un mes año
            Args:
                -excepcion_get: ExceptionMonthYear
                    - prof_id: str
                    - month: int
                    - year: int = today().year
            Returns:
                - List[SpecificSchedule]

        """
        excepcion_dict= excepcion_get.dict()
        excepcion_dict.update({'isCanceling': True})
        return self.filter_month_year(**excepcion_dict)


    def update(self, excepcion: SpecificSchedule, excepcion_update:schema_exception.ExceptionCreate):
        """
        Actualiza hora de inicio y fin 
            Args:
                - excepcion: OBJ: SpecificSchedule
                - excepcion_update: dict
                    - prof_id
                    - day
                    - start
                    - end
            Returns:
                - excepcion
        """
        return super().update(excepcion, excepcion_update)

    def delete(self, excepcion: SpecificSchedule):
        """
        - excepcion: OBJ: SpecificSchedule
        """
        super().delete(excepcion)
        return True

    def commit(self):
        super().commit()