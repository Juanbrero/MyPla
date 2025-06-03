from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import time
from typing import List
from datetime import datetime

#from sqlalchemy import ForeignKeyConstraint

class RecurrentSchedule(Base):
    __tablename__ = "recurrentschedule"
    __table_args__ = (
        CheckConstraint("week_day BETWEEN 0 AND 6 ", name="check_week_valid"),
    )

    week_day: Mapped[int] = mapped_column(primary_key= True)
    start: Mapped[time] = mapped_column(primary_key= True)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"), primary_key= True)
    end: Mapped[time] = mapped_column(nullable= False)
    
    topic_recurrents: Mapped[List["TopicRecurrent"]] = relationship(
        "TopicRecurrent",
        primaryjoin="and_(RecurrentSchedule.prof_id == TopicRecurrent.prof_id, "
                    "RecurrentSchedule.week_day == TopicRecurrent.week_day, "
                    "RecurrentSchedule.start == TopicRecurrent.start)",
        back_populates="recurrent_schedule",
        cascade="all, delete-orphan"
    )
    #create: Mapped[datetime] = mapped_column(default=datetime.today(), server_default='CURRENT_TIMESTAMP') #CURRENT_DATE, CURRENT_TIME 
    #professional: Mapped["Professional"] = relationship(back_populates= "recurrent")

    