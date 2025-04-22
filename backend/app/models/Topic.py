from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class Topic(Base):
    __tablename__ = "topic"

    topic_name: Mapped[str] = mapped_column(primary_key=True)

    profesional_topic: Mapped["ProfesionalTopic"] = relationship(back_populates="topic")