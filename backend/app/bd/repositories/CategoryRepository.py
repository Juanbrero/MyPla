from app.models import Category, Topic
from sqlalchemy.orm import Session
from .Repository import Repository
from sqlalchemy import select, and_


class CategoryRepository(Repository[Category]):
    def __init__(self, session: Session):
        super().__init__(Category, session)
    
    def create(self, data):
        return super().create(**data)