from fastapi import APIRouter
from app.ModuloDePagos import integracionMP

router = APIRouter()

@router.post("/create_preference")
def get_preferenceId():
    return integracionMP.getPreference()