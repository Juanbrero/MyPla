from sqlalchemy import Column, ForeignKey, Float, String, Boolean, TIMESTAMP, func, CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from app.config.database import Base

class Reservation(Base):
    __tablename__ = "reservation"

    day_hour: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    prof_id: Mapped[str] = mapped_column(nullable=False)
    student_id: Mapped[str] = mapped_column(ForeignKey("student.student_id", ondelete="CASCADE"),
                                         nullable=False)
    create: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    cancel: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    state: Mapped[str] = mapped_column(String(10), nullable=False, server_default="pending")
    #class_: Mapped["Class"] = relationship(back_populates="reservation")

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", "student_id", name="pk_reservation"),
        ForeignKeyConstraint(
            ["day_hour", "prof_id"],
            ["meeting.day_hour", "meeting.prof_id"],
            ondelete="CASCADE",
            name="fk_class_meeting"
        ),
        CheckConstraint(
            "state IN ('pending', 'pay', 'cancel_student', 'cancel_professional', 'refund', 'finished')",
            name="check_reservation_state"
        ),
    )