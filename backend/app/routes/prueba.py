from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.Event import Event
from app.models.User import User 

from app.config.database import get_db
#Imports to insert in BD
from sqlalchemy import insert


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}

@router.get("/event")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()
