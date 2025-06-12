from app.models import SpecificSchedule, RecurrentSchedule, TopicSpecific
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, text, cast, Time, func, extract
from .Repository import Repository
from datetime import datetime, date, time


class ExceptionScheduleRepository(Repository[SpecificSchedule]):

    def __init__(self, session: Session):
        super().__init__(SpecificSchedule, session)

    def create(self, data):
        return super().create(**data)
    
    def getSpecificsToRange(self, prof_id: str, day: date, start: time, end: time):
        smt = (
            select(SpecificSchedule)
            .where(
                SpecificSchedule.prof_id == prof_id,
                SpecificSchedule.day == day,
                SpecificSchedule.start < end,
                SpecificSchedule.end > start
            )
        )
        return self.session.execute(smt).scalars().all()
    
    def getAllWithProfessional(self, prof_id: str, day: date, last_day:date):
        stm = (
            select(SpecificSchedule)
            .where(SpecificSchedule.prof_id == prof_id,
                   SpecificSchedule.isCanceling == True,
                   SpecificSchedule.day >= day,
                   SpecificSchedule.day <= last_day)
            .order_by(SpecificSchedule.day.asc())
        )

        return self.session.execute(stm).scalars().all()   

    def getHourDay(self, prof_id:str, day: date, last_day:date):
        """
        Recupera todas excepciones en base a un mes y hasta el siguiente
        """
        stm = (
            select(SpecificSchedule)
            .where(
                SpecificSchedule.prof_id == prof_id,
                SpecificSchedule.day >= day,
                SpecificSchedule.day <= last_day,
                SpecificSchedule.isCanceling == True
            )
            .distinct().order_by(SpecificSchedule.day.asc(), SpecificSchedule.start.asc())
        )

        return self.session.execute(stm).scalars().all() 
    

