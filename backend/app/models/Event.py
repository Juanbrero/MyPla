from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint, Integer, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.config.database import Base

class Event(Base):
    __tablename__ = "event"

    day_hour: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"),
                                         nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    confirm: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", name="pk_meeting"),
    )