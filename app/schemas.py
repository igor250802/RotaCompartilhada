from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

# --- ENUMS (Devem coincidir com o seu Banco de Dados) ---

class ViagemStatus(str, Enum):
    Aberta = "Aberta"
    Em_Curso = "Em Curso"
    Finalizada = "Finalizada"
    Cancelada = "Cancelada"

class ReservaStatus(str, Enum):
    Pendente = "Pendente"
    Aceita = "Aceita"
    Recusada = "Recusada"

# --- SCHEMAS DE USUÁRIO (RF01, RF02) ---

class UserBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None

class UserCreate(UserBase):
    senha: str

class UserResponse(UserBase):
    id_usuario: int
    data_cadastro: datetime

    class Config:
        from_attributes = True

# --- SCHEMAS DE VEÍCULO (Complemento RF03) ---

class VeiculoCreate(BaseModel):
    modelo: str
    placa: str
    cor: Optional[str] = None
    ano: int
    id_proprietario: int

class VeiculoResponse(VeiculoCreate):
    id_veiculo: int

    class Config:
        from_attributes = True

# --- SCHEMAS DE PARADAS (Itinerário) ---

class ParadaBase(BaseModel):
    cidade: str
    ordem_parada: int

class ParadaResponse(ParadaBase):
    id_parada: int
    id_viagem: int

    class Config:
        from_attributes = True

# --- SCHEMAS DE VIAGEM (RF03, RF05) ---

class ViagemCreate(BaseModel):
    id_motorista: int
    id_veiculo: int
    data_hora: datetime
    vagas_totais: int
    itinerario: List[ParadaBase] # Permite criar paradas junto com a viagem

class ViagemResponse(BaseModel):
    id_viagem: int
    id_motorista: int
    id_veiculo: int
    data_hora: datetime
    vagas_totais: int
    status_viagem: ViagemStatus
    
    class Config:
        from_attributes = True

# --- SCHEMAS DE RESERVA (RF04, RF06, RF07) ---

class ReservaCreate(BaseModel):
    id_viagem: int
    id_passageiro: int
    id_parada_embarque: int
    id_parada_desembarque: int
    quantidade_bagagem: int = Field(default=0, ge=0) # RF06: Informar bagagem

class ReservaUpdateStatus(BaseModel):
    status_solicitacao: ReservaStatus # RF07: Motorista aceita ou recusa

class ReservaResponse(ReservaCreate):
    id_reserva: int
    status_solicitacao: ReservaStatus
    data_solicitacao: datetime

    class Config:
        from_attributes = True