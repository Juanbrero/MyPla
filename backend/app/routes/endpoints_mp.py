from fastapi import APIRouter
from app.ModuloDePagos import integracionMP

router = APIRouter()

@router.post("/api/mp/create-preference") #le paso id_reserva por query param
def get_preferenceId():

    return integracionMP.getPreference()