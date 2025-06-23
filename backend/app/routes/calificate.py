from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.controllers.CalificationController import CalificationController
from sqlalchemy.orm import Session
from datetime import datetime
from app.auth0.dependencies import RolesValidator

router = APIRouter(prefix='/api/calificate', tags=['Calificate'])

@router.get('')
def get_class_calificate(db: Session = Depends(get_db), user_info = Depends(RolesValidator(['Alumno', 'Profesional'])) ):
    return CalificationController(db= db).getCalificate(user_info['user_id'], user_info['roles'][0])


@router.patch('/student')
def calificate_professional(day_hour: datetime, prof_id: str, score: int, db: Session= Depends(get_db), user_info = Depends(RolesValidator(['Alumno']))):
    return CalificationController(db= db).calificateProfessional(user_info['user_id'], day_hour, prof_id, score)
