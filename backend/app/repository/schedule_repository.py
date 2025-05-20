from .base import BaseRepository
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional

from sqlalchemy import select, extract
from datetime import time
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class ScheduleRepository(BaseRepository[ModelType]):

    def __init__(self, model, db):
        super().__init__(model, db) 

    def trunc_time(self, horario:time):
        """
        Trunca el horario a horas y minutos
        """
        return time(hour=horario.hour, minute=horario.minute)

    def update(self, schedule_obj:ModelType, schedule_dict:dict ):
        """
        Recibe objeto schedule con los datos de la DB, actualizados para insertar
            Args:
                - schedule: OBJ: ModelType

        """
        schedule_obj.start = schedule_dict['start']
        schedule_obj.end = schedule_dict['end']
        self.commit()
        self.db.refresh(schedule_obj)
        return schedule_obj


    def filter_month_year(self, **kwargs) -> List[ModelType]:
        month = kwargs.pop('month')
        year = kwargs.pop('year')
        return self.db.query(self.model).filter_by(**kwargs).filter(extract("MONTH", self.model.day) == month, 
                                                                    extract("YEAR", self.model.day) == year).all()

    def isCompleteHour(self, start:time, end:time) -> bool:
        """
        Recibe start y end, y compara los minutos para saber si es hora completa
            - True Hora completa
            - False Hora incompleta
        """
        if start.minute != end.minute:
            return False
        return True
    
    def isValidTime(self, start:time, end:time) -> bool:
        """
        Compara start y end (start >= end)
            - True tiempo valido
            - False tiempo invalido
        """
        if end.hour == 0:
            end = time(hour=23, minute=59)

        if start >= end:
            return False
        return True

    def isInclude(self, exist: List[ModelType], start:time, end:time) -> bool:
        """
        compara si el fin ingresado es menor a los inicios en DB, o si el inicio ingresado es mayor o igual al fin en DB
            Args:
                - exist: Lista[Obj]
                - start, end: time
            Retuns
                - True Esta incluido
                - False No esta Incluido
        """
        inicio = time.fromisoformat(start) if type(start) is str else start
        fin = time.fromisoformat(end) if type(end) is str else end
        for dbe in exist:
            if not (fin <= dbe.start or inicio >= dbe.end):
                return True
                break
        return False
    
    def isIncludeUpdate(self):
        raise NotImplementedError
         
    def get_ommit(self, start: time, **kwargs):
        """
        Funcion que recibe el inicio y un diccionario:
            - prof_id
            - day/week
            - [isCanceling]
        y omite el inicio
        """
        omit = self.db.query(self.model).filter_by(**kwargs).filter(self.model.start != start).all()
        return omit