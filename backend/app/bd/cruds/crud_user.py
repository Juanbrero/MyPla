from sqlalchemy.orm import Session
from app.models.User import User
from app.bd.schemas import schema_users
from sqlalchemy import select, insert, delete


def add_user(db: Session, user: schema_users.Users):
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
        user_insert = schema_users.UsersCreate(**user.dict())
        smt = insert(User).values(user_insert.dict())
        response = db.execute(smt)
        if not response is None:
            db.commit()
            return user_insert
    except:
        return {'error':'en la insercion'}

def get_users(db:Session):
    """
    Recupera todos los usuarios
    Arg:
        - db: Session
    Return:
        - List[schema_users.Users]
    """
    return db.query(User).all()


def del_user(db:Session, user:schema_users.UsersBase):
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
    try:
        res = db.get(User, user.dict())
        db.delete(res)
        db.commit()
        return {'info':'OK'}
    except:
        return {'error': 'not delete'}