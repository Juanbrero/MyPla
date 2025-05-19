from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy import select, extract

from datetime import time

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        return self.db.scalars(stmt).all()

    def add(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType):
        self.db.delete(obj)
        self.db.commit()

    def filter_by(self, **kwargs) -> List[ModelType]:
        return self.db.query(self.model).filter_by(**kwargs).all()

    def first_by(self, **kwargs) -> Optional[ModelType]:
        return self.db.query(self.model).filter_by(**kwargs).first()
    
    def filter_month_year(self, **kwargs) -> List[ModelType]:
        month = kwargs.pop('month')
        year = kwargs.pop('year')
        return self.db.query(self.model).filter_by(**kwargs).filter(extract("MONTH", self.model.day) == month, 
                                                                    extract("YEAR", self.model.day) == year).all()

    def update(self):
        raise NotImplemented    

    def get_Q_rows(self, skip:int = 0, limit: int =100):
        """
        Testear si recupera desde el usuario numero skip hasta el limit
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
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
        Prof_id
        start 
        iscanceling
        """
        
        incluido = False
        inicio = start
        fin = end
        for dbe in exist:
            if not (end <= dbe['start'] or start >= dbe['end']):
                return True
        return incluido


    def commit(self):
        self.db.commit()