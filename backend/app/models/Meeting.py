from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.config.database import Base

class Meeting(Base):
    __tablename__ = "meeting"

    day_hour: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"),
                                         nullable=False)
    topic_name: Mapped[str] = mapped_column(ForeignKey("topic.topic_name", ondelete="CASCADE"),
                                         nullable=False)

    #professional: Mapped["Professional"] = relationship(back_populates="meeting")
    #topic: Mapped["Topic"] = relationship(back_populates="meeting")
    #class_: Mapped["Class"] = relationship(back_populates="meeting")

    __table_args__ = (
        PrimaryKeyConstraint("day_hour", "prof_id", name="pk_meeting"),
    )