from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import time
from typing import List

#from sqlalchemy import ForeignKeyConstraint

class RecurrentSchedule(Base):
    __tablename__ = "recurrentschedule"
    __table_args__ = (
        CheckConstraint("week_day BETWEEN 1 AND 7 ", name="check_week_valid"),
    )

    week_day: Mapped[int] = mapped_column(primary_key= True)
    start: Mapped[time] = mapped_column(primary_key= True)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"), primary_key= True)
    end: Mapped[time] = mapped_column(nullable= False)
    #create: Mapped[datetime] = mapped_column(default=datetime.today(), server_default='CURRENT_TIMESTAMP') #CURRENT_DATE, CURRENT_TIME 
    professional: Mapped["Professional"] = relationship(back_populates= "recurrent")

    