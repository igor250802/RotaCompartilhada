from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/history", tags=["Histórico"])

@router.get("/passenger/{id_usuario}", response_model=list[schemas.ReservaResponse])
def historico_como_passageiro(id_usuario: int, db: Session = Depends(database.get_db)):
    """Retorna todas as reservas (solicitações) que o usuário fez como passageiro"""
    return db.query(models.Reserva).filter(models.Reserva.id_passageiro == id_usuario).all()

@router.get("/driver/{id_usuario}", response_model=list[schemas.ViagemResponse])
def historico_como_motorista(id_usuario: int, db: Session = Depends(database.get_db)):
    """Retorna todas as viagens que o usuário criou como motorista"""
    return db.query(models.Viagem).filter(models.Viagem.id_motorista == id_usuario).all()