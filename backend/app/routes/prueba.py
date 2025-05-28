from fastapi import APIRouter


router = APIRouter()

@router.get("/api/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}
