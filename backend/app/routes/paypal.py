from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ModuloDePagos.integracionPayPal import create_order, capture_order

router = APIRouter()

# Simulación de productos (reemplazable con DB)
PRODUCTOS = {
    "curso_python": {"descripcion": "Curso de Python", "precio": "100.00"},
    "suscripcion_mensual": {"descripcion": "Suscripción mensual", "precio": "15.00"},
    "ebook": {"descripcion": "Ebook avanzado", "precio": "9.99"},
}

class ProductRequest(BaseModel):
    product_id: str

class CaptureRequest(BaseModel):
    orderID: str

@router.post("/create-order")
def api_create_order(data: ProductRequest):
    producto = PRODUCTOS.get(data.product_id)
    if not producto:
        raise HTTPException(status_code=400, detail="Producto no válido")

    return create_order(amount=producto["precio"])

@router.post("/capture-order")
def api_capture_order(data: CaptureRequest):
    return capture_order(order_id=data.orderID)
