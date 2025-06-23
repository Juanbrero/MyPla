from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.controllers.CalificationController import CalificationController
from sqlalchemy.orm import Session
from datetime import datetime
from app.auth0.dependencies import RolesValidator
from app.bd.schemas import schema_calificate

router = APIRouter(prefix='/api/calificate', tags=['Calificate'])

@router.get('', response_model=schema_calificate.GetCalification)
def get_class_calificate(db: Session = Depends(get_db), user_info = Depends(RolesValidator(['Alumno', 'Profesional'])) ):
    """
        Recibe TOKEN
    """
    return CalificationController(db= db).getCalificate(user_info['user_id'], user_info['roles'][0])


@router.patch('/student')
def calificate_professional(calificateS: schema_calificate.Calificate, db: Session= Depends(get_db), user_info = Depends(RolesValidator(['Alumno']))):
    return CalificationController(db= db).calificateProfessional(user_info['user_id'], calificateS)
