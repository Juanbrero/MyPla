from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import time

class TopicRecurrent(Base):
    __tablename__ = "topicrecurrent"
    __table_args__= (
        ForeignKeyConstraint(
        ['prof_id', 'topic_name'],
        ['professionaltopic.prof_id', 'professionaltopic.topic_name'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    ), 
    ForeignKeyConstraint(
        ['prof_id', 'week_day', 'start'],
        ['recurrentschedule.prof_id', 'recurrentschedule.week_day', 'recurrentschedule.start'],
        onupdate='CASCADE',
        ondelete='CASCADE'
    ),
    )

    prof_id: Mapped[str] = mapped_column(primary_key=True)
    topic_name: Mapped[str] = mapped_column(primary_key=True)
    start: Mapped[time] = mapped_column(primary_key=True)
    week_day: Mapped[int] = mapped_column(primary_key=True)

    topic: Mapped['ProfessionalTopic'] = relationship(back_populates='recurrent_topic')


