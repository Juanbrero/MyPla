from fastapi import APIRouter, Depends
from app.ModuloDePagos import integracionMP
from app.config.database import get_db
from app.auth0.dependencies import RolesValidator
from ..controllers.PayController import PayController
from app.bd.schemas import schema_reservation
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/pay")


@router.post("/initial-paypal", tags=['Pay'])
def get_preferenceId(db: Session = Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    return PayController(db=db).initialPay(user_info["user_id"])

@router.post("/mp_preference", tags=['Pay'])
def get_prerence(db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    return PayController(db= db).createPreference(user_info["user_id"])

@router.get("/pending", tags=['Pay'])
def get_pay_pending(db:Session = Depends(get_db)):#, user_info = Depends(RolesValidator(["Administrador"]))):
    return PayController(db=db).getPayPending()

@router.put("/pending", tags=['Pay'])
def modify_pay_pending(pay: schema_reservation.PayPending, db:Session = Depends(get_db)):#, user_info = Depends(RolesValidator(["Administrador"]))):
    return PayController(db=db).modifyPayPending(pay)