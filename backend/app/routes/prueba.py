from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.User import User
from app.config.database import get_db

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()