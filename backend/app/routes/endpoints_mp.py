from fastapi import APIRouter
from ModuloDePagos import integracionMP

router = APIRouter()

@router.post("/create_preference")
def get_preferenceId():
    return integracionMP.getPreference()