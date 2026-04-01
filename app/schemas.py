from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Esquema para criar usuário (Entrada)
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: Optional[str] = None

# Esquema para mostrar usuário (Saída - sem a senha!)
class UserResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    
    class Config:
        from_attributes = True