from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

# Definindo Enums conforme seu SQL
class ViagemStatus(str, enum.Enum):
    Aberta = "Aberta"
    Em_Curso = "Em Curso"
    Finalizada = "Finalizada"
    Cancelada = "Cancelada"

class ReservaStatus(str, enum.Enum):
    Pendente = "Pendente"
    Aceita = "Aceita"
    Recusada = "Recusada"

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    telefone = Column(String(20))
    data_cadastro = Column(TIMESTAMP, server_default=func.now())

class Veiculo(Base):
    __tablename__ = "veiculos"
    id_veiculo = Column(Integer, primary_key=True, index=True)
    id_proprietario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    modelo = Column(String(50), nullable=False)
    placa = Column(String(10), unique=True, nullable=False)
    cor = Column(String(30))
    ano = Column(Integer, nullable=False)

class Viagem(Base):
    __tablename__ = "viagens"
    id_viagem = Column(Integer, primary_key=True, index=True)
    id_motorista = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"))
    data_hora = Column(DateTime, nullable=False)
    vagas_totais = Column(Integer, nullable=False)
    status_viagem = Column(Enum(ViagemStatus), default=ViagemStatus.Aberta)