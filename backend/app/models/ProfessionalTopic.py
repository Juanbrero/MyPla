from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from typing import List

class ProfessionalTopic(Base):
    __tablename__ = "professionaltopic"
    __table_args__ = (
        CheckConstraint('price_class > 0 ', name='check_price_valid'),
    )


    topic_name: Mapped[str] = mapped_column(ForeignKey("topic.topic_name", ondelete="CASCADE"), primary_key=True)
    prof_id: Mapped[int] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"), primary_key= True)
    price_class: Mapped[float] = mapped_column(nullable=False)


    professional: Mapped["Professional"] = relationship(back_populates= "topics",)
    topic: Mapped["Topic"] = relationship(back_populates="professional_topic")

    recurrent_topic: Mapped[List["TopicRecurrent"]] = relationship(back_populates="topic", cascade='all, delete-orphan')
    specific_topic: Mapped[List["TopicSpecific"]] = relationship(back_populates="topic", cascade='all, delete-orphan')
