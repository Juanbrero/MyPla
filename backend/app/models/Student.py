from sqlalchemy import Column, Integer, String, text, Float, CheckConstraint, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.config.database import Base

class Student(Base):
    __tablename__  = "student"

    student_id: Mapped[str]  = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"),
                                    primary_key=True,
                                    index=True)
    score: Mapped[float] = mapped_column(default=0, server_default=text('0'))
    
    cvu: Mapped[str] = mapped_column(String, nullable=False)

    #user: Mapped['User'] = relationship(back_populates='student')
    
    #reservation: Mapped[List['Reservation']] = relationship(back_populates='student')
