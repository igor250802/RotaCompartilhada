from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

# --- ENUMS (Exatamente como no seu SQL) ---

class ViagemStatus(str, enum.Enum):
    Aberta = "Aberta"
    Em_Curso = "Em Curso"
    Finalizada = "Finalizada"
    Cancelada = "Cancelada"

class ReservaStatus(str, enum.Enum):
    Pendente = "Pendente"
    Aceita = "Aceita"
    Recusada = "Recusada"

# --- MODELOS ---

class Usuario(Base):
    __tablename__ = "usuarios" # Conforme script SQL 

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    telefone = Column(String(20))
    data_cadastro = Column(TIMESTAMP, server_default=func.now())

    # Relacionamentos
    veiculos = relationship("Veiculo", back_populates="proprietario", cascade="all, delete")
    viagens = relationship("Viagem", back_populates="motorista")

class Veiculo(Base):
    __tablename__ = "veiculos" # Conforme script SQL 

    id_veiculo = Column(Integer, primary_key=True, index=True)
    id_proprietario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    modelo = Column(String(50), nullable=False)
    placa = Column(String(10), unique=True, nullable=False)
    cor = Column(String(30))
    ano = Column(Integer, nullable=False)

    proprietario = relationship("Usuario", back_populates="veiculos")

class Viagem(Base):
    __tablename__ = "viagens" # Conforme script SQL 

    id_viagem = Column(Integer, primary_key=True, index=True)
    id_motorista = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    vagas_totais = Column(Integer, nullable=False)
    status_viagem = Column(Enum(ViagemStatus), server_default="Aberta")

    motorista = relationship("Usuario", back_populates="viagens")
    itinerario = relationship("Parada", back_populates="viagem", cascade="all, delete")

class Parada(Base):
    __tablename__ = "paradas" # Conforme script SQL 

    id_parada = Column(Integer, primary_key=True, index=True)
    id_viagem = Column(Integer, ForeignKey("viagens.id_viagem", ondelete="CASCADE"), nullable=False)
    cidade = Column(String(100), nullable=False)
    ordem_parada = Column(Integer, nullable=False)

    viagem = relationship("Viagem", back_populates="itinerario")

class Reserva(Base):
    __tablename__ = "reservas" # Conforme script SQL 

    id_reserva = Column(Integer, primary_key=True, index=True)
    id_viagem = Column(Integer, ForeignKey("viagens.id_viagem", ondelete="CASCADE"), nullable=False)
    id_passageiro = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_parada_embarque = Column(Integer, ForeignKey("paradas.id_parada"), nullable=False)
    id_parada_desembarque = Column(Integer, ForeignKey("paradas.id_parada"), nullable=False)
    quantidade_bagagem = Column(Integer, default=0, nullable=False) # Atende RF06 
    status_solicitacao = Column(Enum(ReservaStatus), server_default="Pendente") # Atende RF07 
    data_solicitacao = Column(TIMESTAMP, server_default=func.now())