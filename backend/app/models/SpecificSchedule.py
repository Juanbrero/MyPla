from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

from datetime import date
from datetime import time

class SpecificSchedule(Base):
    __tablename__ = "specificschedule"

    day: Mapped[date] = mapped_column(primary_key=True)
    start: Mapped[time] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profesional.user_id",ondelete="CASCADE"), primary_key=True)
    end: Mapped[time] = mapped_column(nullable=False)
    isCanceling: Mapped[bool] = mapped_column(default=False)

    profesional: Mapped["Profesional"] = relationship(back_populates="specific")

   