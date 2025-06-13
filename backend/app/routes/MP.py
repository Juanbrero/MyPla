from fastapi import APIRouter, Depends
from app.ModuloDePagos import integracionMP
from app.config.database import get_db
from app.auth0.dependencies import RolesValidator
from ..controllers.PayController import PayController
from app.bd.schemas import schema_reservation
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/api/mp/create-preference", tags=['Pay'])
def get_prerence(db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    return PayController(db= db).createPreference(user_info["user_id"])