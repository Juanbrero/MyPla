from fastapi import APIRouter, Depends, HTTPException
from alembic import command
from alembic.config import Config

router = APIRouter()

@router.post("/api/reset_db")
def reset_db():
    try:
        alembic_cfg = Config("alembic.ini")
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        return {"status": "Base de datos reseteada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
