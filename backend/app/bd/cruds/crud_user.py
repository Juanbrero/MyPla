from sqlalchemy.orm import Session
from app.models.User import User
from app.bd.schemas import schema_users
from sqlalchemy import select, insert, delete
from .crud_base import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db:Session):
        self.db = db

    def add_user(self, user: schema_users.Users):
        """
        Agrega un usuario a la BD

        Args:
            - db: Session
            - user: schema_users.Users
                - user_id: str
                - name: str
        Return:
            {user_id: str, name:str}
            {error: str}
        """
        try:
            user_insert = User(**user.dict())
            self.db.add(user_insert)
            self.db.commit()
            self.db.refresh(user_insert)
            return user_insert
        except:
            return {'error':'On insert User'}
        
    def get_user_id(self, user:schema_users.Users):
        response = self.db.query(User).filter(User.user_id == user.user_id).first()
        return response

    def get_users(self):
        """
        Recupera todos los usuarios
        Arg:
            - db: Session
        Return:
            - List[schema_users.Users]
        """
        return self.db.query(User).all()


    def del_user(self, user:schema_users.UsersBase):
        """
        Elimina un usuario
        Args:
            - db: Session
            - user: schema_users.UserBase
                - user_id: str
        Return:
            {info: str}
            {error: str}
        """
        res = self.db.get(User, user.dict())
        if res is None:
            return False
        self.db.delete(res)
        self.db.commit()
        return True