from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from ..controllers.AvailableController import AvailableController
from app.bd.schemas import schema_response
from datetime import date


router = APIRouter(prefix='/api/available')

@router.get('/professionals', tags=['Available'], response_model= schema_response.ResponseProfessional )
def get_available_prof(prof_id: str, db:Session = Depends(get_db)):

    return AvailableController(db= db).getProfessionalAvailable(prof_id)


@router.get('/student', tags=['Available'], response_model= schema_response.ResponseAlumno)
def get_available_student(prof_id: str, day: date | None = None, db: Session= Depends(get_db)):
    
    return AvailableController(db= db).getStudentAvailable(prof_id, day)