from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy import select



ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        return self.db.scalars(stmt).all()

    def add(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType):
        self.db.delete(obj)
        self.db.commit()

    def filter_by(self, **kwargs) -> List[ModelType]:
        return self.db.query(self.model).filter_by(**kwargs).all()

    def first_by(self, **kwargs) -> Optional[ModelType]:
        return self.db.query(self.model).filter_by(**kwargs).first()
    

    def update(self):
        raise NotImplementedError    

    def get_Q_rows(self, skip:int = 0, limit: int =100):
        """
        Testear si recupera desde el usuario numero skip hasta el limit
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    

    def commit(self):
        self.db.commit()