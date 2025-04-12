from pydantic import BaseModel

class UserTypePayload(BaseModel):
    user_id: str
    tipo_usuario: str  # "alumno" o "profesional"