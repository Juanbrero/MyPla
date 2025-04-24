from sqlalchemy import Column, Integer, String, text, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
'''
from sqlalchemy import ForeignKey
'''
from app.config.database import Base

class Profesional(Base):
    __tablename__  = "profesional"

    user_id: Mapped[int]  = mapped_column(primary_key=True,
                                     index=True)
    score: Mapped[float] = mapped_column(Float, default=0, server_default=text('0'))

    specific: Mapped[List["SpecificSchedule"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    recurrent: Mapped[List["RecurrentSchedule"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    topics: Mapped[List["ProfesionalTopic"]] = relationship(back_populates="profesional",cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('score >= 0 AND 5 <= score', name='check_score_valid'),
    )
