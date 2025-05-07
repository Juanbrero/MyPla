from sqlalchemy import Column, Integer, String, text, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
'''
from sqlalchemy import ForeignKey
'''
from app.config.database import Base

class Professional(Base):
    __tablename__  = "professional"

    prof_id: Mapped[str]  = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"),
                                    primary_key=True,
                                    index=True)
    score: Mapped[float] = mapped_column(default=0, server_default=text('0'))

    user: Mapped['User'] = relationship(back_populates='professional')
    
    specific: Mapped[List["SpecificSchedule"]] = relationship(back_populates="professional", cascade="all, delete-orphan")
    recurrent: Mapped[List["RecurrentSchedule"]] = relationship(back_populates="professional", cascade="all, delete-orphan")
    topics: Mapped[List["ProfessionalTopic"]] = relationship(back_populates="professional", cascade="all, delete-orphan")
    #invite: Mapped[List['Invite']] = relationship(back_populates='invite', cascade='all, delete-orphan')


    __table_args__ = (
        CheckConstraint('score BETWEEN 0 AND 5', name='check_score_valid'),
    )
