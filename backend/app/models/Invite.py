from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint, Integer, Boolean, Float, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.config.database import Base

class Invite(Base):
    __tablename__ = "invite"

    day_hour: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"),
                                         nullable=False)
    invite_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"),
                                         nullable=False)
    accept: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", "invite_id", name="pk_invite"),
        ForeignKeyConstraint(
            ["day_hour", "prof_id"],
            ["event.day_hour", "event.prof_id"],
            ondelete="CASCADE",
            name="fk_invite_event"
        ),
        ForeignKeyConstraint(
            ["invite_id"],
            ["professional.prof_id"],
            ondelete="CASCADE",
            name="fk_invite_professional"
        )
    )