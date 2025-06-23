from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey

class Topic(Base):
    __tablename__ = "topic"

    topic_name: Mapped[str] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String, ForeignKey(column="category.category_name", name="fk_topic_category", ondelete="CASCADE", onupdate="CASCADE")
                                          , nullable=False)

    #create: Mapped[datetime] = mapped_column(default=datetime.today(), server_default='CURRENT_TIMESTAMP') #CURRENT_DATE, CURRENT_TIME 

    #professional_topic: Mapped[List["ProfessionalTopic"]] = relationship(back_populates="topic", cascade='all, delete-orphan')