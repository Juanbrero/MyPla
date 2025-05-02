from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import time, date

class TopicSpecific(Base):
    __tablename__ = "topicspecific"
    __table_args__= (
        ForeignKeyConstraint(
        ['prof_id', 'topic_name'],
        ['professionaltopic.prof_id', 'professionaltopic.topic_name'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    ), 
    ForeignKeyConstraint(
        ['prof_id', 'day', 'start'],
        ['specificschedule.prof_id', 'specificschedule.day', 'specificschedule.start'],
        onupdate='CASCADE',
        ondelete='CASCADE'
    ),
    )

    prof_id: Mapped[str] = mapped_column(primary_key=True)
    topic_name: Mapped[str] = mapped_column(primary_key=True)
    start: Mapped[time] = mapped_column(primary_key=True)
    day: Mapped[date] = mapped_column(primary_key=True)

    topic: Mapped['ProfessionalTopic'] = relationship(back_populates='specific_topic')


