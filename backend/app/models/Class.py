from sqlalchemy import Column, ForeignKey, Float, TIMESTAMP, CheckConstraint, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from app.config.database import Base

class Class(Base):
    __tablename__ = "class"

    day_hour: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    prof_id: Mapped[str] = mapped_column(nullable=False)

    calificate_teacher: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calificate_student: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    #meeting: Mapped["Meeting"] = relationship(back_populates="class")

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", name="pk_class"),
        ForeignKeyConstraint(
            ["day_hour", "prof_id"],
            ["meeting.day_hour", "meeting.prof_id"],
            ondelete="CASCADE",
            name="fk_class_meeting"
        ),
        CheckConstraint('calificate_teacher BETWEEN 0 AND 5', name='check_calificate_teacher_valid'),
        CheckConstraint('calificate_student BETWEEN 0 AND 5', name='check_calificate_student_valid'),
    )