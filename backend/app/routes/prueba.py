from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#Scheme table
from app.models.Event import Event
from app.models.User import User 

from app.config.database import get_db,init_db
#Imports to insert in BD
from sqlalchemy import insert

router = APIRouter()

@router.get("/")
def read_root():
    init_db()
    return {"message": "¡Hola, FastAPI está funcionando!"}

@router.get("/event")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.get("/add-user1")
def set_table(db: Session = Depends(get_db)):
    db.scalars(
        insert(User).values(name="PEPE")
    )
    db.commit()
    return db.query(User).all()


@router.get("/add-user2")
def set_table(db: Session = Depends(get_db)):
    db.scalars(
        insert(User).values({"name":"Luis"})
    )
    db.commit()
    return db.query(User).all()

@router.get("/add-users")
def set_table(db: Session = Depends(get_db)):
    db.execute(
        insert(User),[
            {"name":"USER1"},
            {"name":"USER2"}
            ]
    )
    db.commit()
    return db.query(User).all()