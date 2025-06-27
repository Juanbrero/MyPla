from sqlalchemy import Column, String, text, CheckConstraint, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, Float, Boolean, false

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import ForeignKey
from datetime import datetime

from app.config.database import Base

class Cancelation(Base):
    __tablename__ = "cancelation"

    prof_id: Mapped[str] = mapped_column(ForeignKey(name="fk_professional_cancelation",column="professional.prof_id", ondelete="CASCADE", onupdate="CASCADE"), 
                                         nullable=False)
    
    student_id: Mapped[str] = mapped_column(ForeignKey(name="fk_student_ cancelation", column="student.student_id", ondelete="CASCADE", onupdate="CASCADE"), 
                                            nullable=False)
    
    cancel_time: Mapped[datetime] =  mapped_column(TIMESTAMP, nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    day_hour: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    refund: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", "student_id", name="pk_cancel"),
        CheckConstraint(
            "state IN ( 'cancel_student', 'cancel_professional')",
            name="check_cancel_state"
        ),
    )