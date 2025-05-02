from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

from datetime import date, time, datetime

class SpecificSchedule(Base):
    __tablename__ = "specificschedule"

    day: Mapped[date] = mapped_column(primary_key=True)
    start: Mapped[time] = mapped_column(primary_key=True)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"), primary_key=True)
    end: Mapped[time] = mapped_column(nullable=False)
    #create: Mapped[datetime] = mapped_column(default=datetime.today(), server_default='CURRENT_TIMESTAMP') #CURRENT_DATE, CURRENT_TIME 
    isCanceling: Mapped[bool] = mapped_column(default=False)

    professional: Mapped["Professional"] = relationship(back_populates="specific")

   