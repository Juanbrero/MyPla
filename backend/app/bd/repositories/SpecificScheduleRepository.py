from app.models import SpecificSchedule, RecurrentSchedule, TopicSpecific
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, text, cast, Time, func
from .Repository import Repository
from datetime import datetime, date, time

class SpecificScheduleRepository(Repository[SpecificSchedule]):
    def __init__(self, session: Session):
        super().__init__(SpecificSchedule, session)
    
    def create(self, data):
        return super().create(**data)
    
    def getSpecificToClass (self, prof_id: str, topic: str, day_hour: datetime):
        target_day = day_hour.date()
        target_time = day_hour.time()
        smt = (
            select(SpecificSchedule)
            .join(SpecificSchedule.topic_specifics)
            .where(
                SpecificSchedule.isCanceling == False,
                SpecificSchedule.prof_id == prof_id,
                TopicSpecific.topic_name == topic,
                SpecificSchedule.day == target_day,
                SpecificSchedule.start <= target_time,
                cast(
                    func.cast(SpecificSchedule.end, Time) - func.cast('01:00:00', Time),
                    Time
                ) >= target_time,
            )
            .options(selectinload(SpecificSchedule.topic_specifics))
            .distinct()
        )
        return self.session.execute(smt).scalars().all()

    def getExceptionToClass (self, prof_id: str, day_hour: datetime):
        target_day = day_hour.date()
        target_time = day_hour.time()
        smt = (
            select(SpecificSchedule)
            .where(
                SpecificSchedule.isCanceling == True,
                SpecificSchedule.prof_id == prof_id,
                SpecificSchedule.day == target_day,
                SpecificSchedule.start <= target_time,
                cast(
                    func.cast(SpecificSchedule.end, Time) - func.cast('01:00:00', Time),
                    Time
                ) >= target_time,
            )
        )
        return self.session.execute(smt).scalars().all()
    
    def getSpecificsToRange (self, prof_id: str, day: date, start: time, end: time):
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