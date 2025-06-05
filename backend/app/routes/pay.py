from fastapi import APIRouter
from app.ModuloDePagos import integracionMP

router = APIRouter()

@router.post("/api/mp/create-preference")
def get_preferenceId():
    return integracionMP.getPreference()