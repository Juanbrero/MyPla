from sqlalchemy import Column, Integer, String
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
    score: Mapped[int] = mapped_column(default= 0)

    #dias: Mapped[List["Dia"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    specific: Mapped[List["SpecificSchedule"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    recurrent: Mapped[List["RecurrentSchedule"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")