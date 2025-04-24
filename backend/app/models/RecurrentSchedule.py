from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import time
from typing import List

#from sqlalchemy import ForeignKeyConstraint

class RecurrentSchedule(Base):
    __tablename__ = "recurrentschedule"
    __table_args__ = (
        CheckConstraint("name_day IN ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')", name="check_name_valid"),
    )

    name_day: Mapped[str] = mapped_column(primary_key= True)
    start: Mapped[time] = mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profesional.user_id", ondelete="CASCADE"), primary_key= True)
    end: Mapped[time] = mapped_column(nullable= False)

    profesional: Mapped["Profesional"] = relationship(back_populates= "recurrent")
    #recurrent_topic: Mapped["TopicRecurrent"] = relationship(back_populates="recurrent", cascade="all, delete-orphan")
    