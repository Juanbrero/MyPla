from app.models import RecurrentSchedule, TopicRecurrent
from sqlalchemy.orm import Session, selectinload
from .Repository import Repository
from sqlalchemy import select, cast, Time, func, and_
from datetime import datetime
from app.bd.bd_utils import week_convert

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
        ).order_by(RecurrentSchedule.week_day, RecurrentSchedule.start)
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
        target_day = week_convert(day_hour.isoweekday())
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
                    func.cast(RecurrentSchedule.end, Time) - func.cast("01:00:00", Time),
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
    
    def getException(self, specific: dict):
        """
        Recupera todos los horarios de un dia recurrente que esten abarcados por una excepcion
        """
        stm = (
            select(RecurrentSchedule)
            .where(
                RecurrentSchedule.week_day == specific['week'],
                RecurrentSchedule.prof_id == specific['prof_id'],
                RecurrentSchedule.start <= specific['start'],
                specific['end'] <= RecurrentSchedule.end
            )
        )
        return self.session.execute(stm).scalars().all()
    
    def getSpecific(self, specific: dict):
        """
        Recupera todos los horarios de un dia recurrente que esten abarcados por un especifico
        """
        stm = (
            select(RecurrentSchedule)
            .where(
                RecurrentSchedule.week_day == specific['week'],
                RecurrentSchedule.prof_id == specific['prof_id'],
                and_(
                    specific['start'] < RecurrentSchedule.end,
                    specific['end'] > RecurrentSchedule.start,
                    specific['end'] != RecurrentSchedule.start,
                    specific['start'] != RecurrentSchedule.end
                )
            )
        )
        return self.session.execute(stm).scalars().all()