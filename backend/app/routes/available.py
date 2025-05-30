from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from ..controllers.AvailableController import AvailableController
from app.bd.schemas import schema_response
from datetime import date
from json import loads
from app.auth0.dependencies import RolesValidator


router = APIRouter(prefix='/api/available')

@router.get('/professionals', tags=['Available'], response_model= schema_response.ResponseProfessional )
def get_available_prof( db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):

    return AvailableController(db= db).getProfessionalAvailable(user_info["user_id"])


@router.get('/student', tags=['Available'], response_model= schema_response.ResponseAlumno)
def get_available_student(db: Session= Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    
    return AvailableController(db= db).getStudentAvailable(user_info["user_id"])

