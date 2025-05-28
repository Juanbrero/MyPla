from app.models import SpecificSchedule, RecurrentSchedule, TopicSpecific
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, text, cast, Time, func
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
    
    def getAllWithProfessional(self, prof_id: str):
        stm = (
            select(SpecificSchedule)
            .where(SpecificSchedule.prof_id == prof_id,
                   SpecificSchedule.isCanceling == True)
        )

        return self.session.execute(stm).scalars().all()    
    

