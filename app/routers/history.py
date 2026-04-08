from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/history", tags=["Histórico"])

# RF08: Visualizar histórico como Motorista
@router.get("/driver/{id_usuario}", response_model=list[schemas.ViagemResponse])
def obter_historico_motorista(id_usuario: int, db: Session = Depends(database.get_db)):
    # Busca todas as viagens onde o usuário é o motorista, ordenando pelas mais recentes
    viagens = db.query(models.Viagem).filter(
        models.Viagem.id_motorista == id_usuario
    ).order_by(models.Viagem.data_hora.desc()).all()
    
    if not viagens:
        raise HTTPException(status_code=404, detail="Nenhum histórico de viagens como motorista encontrado.")
    return viagens

# RF08: Visualizar histórico como Passageiro
@router.get("/passenger/{id_usuario}", response_model=list[schemas.ReservaResponse])
def obter_historico_passageiro(id_usuario: int, db: Session = Depends(database.get_db)):
    # Busca todas as reservas feitas por este usuário
    reservas = db.query(models.Reserva).filter(
        models.Reserva.id_passageiro == id_usuario
    ).order_by(models.Reserva.data_solicitacao.desc()).all()

    if not reservas:
        raise HTTPException(status_code=404, detail="Nenhum histórico de reservas como passageiro encontrado.")
    return reservas