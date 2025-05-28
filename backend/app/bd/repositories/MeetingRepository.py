from app.models import Meeting
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, Time, cast, func, or_
from datetime import datetime, date, time, timedelta

class MeetingRepository(Repository[Meeting]):
    def __init__(self, session: Session):
        super().__init__(Meeting, session)
    
    def create(self, data):
        return super().create(**data)
    
    def getMeetingToRange (self, prof_id: str, day: date, start: time, end: time):
        start_dt = datetime.combine(day, start)
        end_dt = datetime.combine(day, end)
        
        smt = (
            select(Meeting)
            .where(
                Meeting.prof_id == prof_id,
                Meeting.day_hour < end_dt,
                (Meeting.day_hour + timedelta(hours=1)) > start_dt
            )
        )
        return self.session.execute(smt).scalars().all()
    
    def getMeetingRecurrent(self, prof_id: str, week_day: int, start:time, end:time):
       
        smt = (
            select(Meeting)
            .where(
                Meeting.prof_id == prof_id,
                #Meeting.day_hour >= func.now(),
                func.extract('dow', Meeting.day_hour) == week_day, or_(
                cast(Meeting.day_hour + timedelta(hours= 1), Time) > start,
                cast(Meeting.day_hour, Time) < end)
            )
        )
        return self.session.execute(smt).scalars().all()