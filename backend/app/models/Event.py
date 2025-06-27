from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint, Integer, Boolean, Float, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.config.database import Base

class Event(Base):
    __tablename__ = "event"

    day_hour: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    prof_id: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    confirm: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    cancel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    title: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", name="pk_event"),
        ForeignKeyConstraint(
            ["day_hour", "prof_id"],
            ["meeting.day_hour", "meeting.prof_id"],
            ondelete="CASCADE",
            name="fk_class_meeting"
        )
    )