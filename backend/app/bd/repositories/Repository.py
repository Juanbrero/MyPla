from typing import TypeVar, Generic, Type, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
T = TypeVar("T", bound=Base)

class Repository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        print(vars(instance))
        self.session.add(instance)
        return instance

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def get_by(self, filters: Dict[str, Any]) -> List[T]:
        query = self.session.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.all()

    def update(self, values: Dict[str, Any], filters: Dict[str, Any]) -> int:
        query = self.session.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        updated = query.update(values, synchronize_session="fetch")
        return updated

    def delete(self, filters: Dict[str, Any]) -> int:
        query = self.session.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        deleted = query.delete(synchronize_session="fetch")
        return deleted
