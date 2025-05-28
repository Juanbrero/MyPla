from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class ProfesionalTopic(Base):
    __tablename__ = "profesionaltopic"

    topic_name: Mapped[str] = mapped_column(ForeignKey("topic.topic_name", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profesional.user_id", ondelete="CASCADE"), primary_key= True)


    profesional: Mapped["Profesional"] = relationship(back_populates= "topics")
    topic: Mapped["Topic"] = relationship(back_populates="profesional_topic")
