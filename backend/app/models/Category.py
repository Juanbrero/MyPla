from sqlalchemy import Column, String, text, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
'''
from sqlalchemy import ForeignKey
'''
from app.config.database import Base


class Category(Base):
    __tablename__ = "category"

    category_name: Mapped[str] = mapped_column(String, primary_key= True)