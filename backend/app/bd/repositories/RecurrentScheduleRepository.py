from app.models import RecurrentSchedule, TopicRecurrent
from sqlalchemy.orm import Session, selectinload
from .Repository import Repository
from sqlalchemy import select, cast, Time, func
from datetime import datetime

class RecurrentScheduleRepository(Repository[RecurrentSchedule]):
    def __init__(self, session: Session):
        super().__init__(RecurrentSchedule, session)
    
    def create(self, data):
        return super().create(**data)
        
    def getRecurrentsWithTopics (self, prof_id: str):
        smt = (
            select(RecurrentSchedule)
            .where(RecurrentSchedule.prof_id == prof_id)
            .options(selectinload(RecurrentSchedule.topic_recurrents))
        )
        return self.session.execute(smt).scalars().all()
    
    def getRecurrentsSpecificTopic (self, prof_id: str, topic: str):
        smt = (
            select(RecurrentSchedule)
            .join(RecurrentSchedule.topic_recurrents)
            .where(
                RecurrentSchedule.prof_id == prof_id,
                TopicRecurrent.topic_name == topic
            )
            .options(selectinload(RecurrentSchedule.topic_recurrents))
            .distinct()
        )
        
    def getRecurrentToClass (self, prof_id: str, topic: str, day_hour: datetime):
        target_day = day_hour.isoweekday()
        target_time = day_hour.time()
        smt = (
            select(RecurrentSchedule)
            .join(RecurrentSchedule.topic_recurrents)
            .where(
                RecurrentSchedule.prof_id == prof_id,
                TopicRecurrent.topic_name == topic,
                RecurrentSchedule.week_day == target_day,
                RecurrentSchedule.start <= target_time,
                cast(
                    func.cast(RecurrentSchedule.end, Time) - func.cast('01:00:00', Time),
                    Time
                ) >= target_time
            )
            .options(selectinload(RecurrentSchedule.topic_recurrents))
            .distinct()
        )
        return self.session.execute(smt).scalars().all()
    
   
    def getOmmit(self, recurrent:dict):
        """
        Recupera todos los horarios de un día de la semana, omitiendo el valor del start ingresado
        """
        stm =(
            select(RecurrentSchedule)
            .where(RecurrentSchedule.week_day == recurrent['week_day'],
                   RecurrentSchedule.prof_id == recurrent['prof_id'],
                   RecurrentSchedule.start != recurrent['start'])
        )

        return self.session.execute(stm).scalars().all()