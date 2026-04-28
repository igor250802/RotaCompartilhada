from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservas"])

@router.post("/", response_model=schemas.ReservaResponse)
def solicitar_reserva(obj_in: schemas.ReservaCreate, db: Session = Depends(database.get_db)):
    # 1. Verificar se a viagem existe
    viagem = db.query(models.Viagem).filter(models.Viagem.id_viagem == obj_in.id_viagem).first()
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    
    # 2. Verificar se ainda há vagas
    if viagem.vagas_totais <= 0:
        raise HTTPException(status_code=400, detail="Esta carona já não possui vagas disponíveis")

    # 3. Criar a reserva com status Pendente
    nova_reserva = models.Reserva(
        id_viagem=obj_in.id_viagem,
        id_passageiro=obj_in.id_passageiro,
        id_parada_embarque=obj_in.id_parada_embarque,
        id_parada_desembarque=obj_in.id_parada_desembarque,
        quantidade_bagagem=obj_in.quantidade_bagagem,
        status_solicitacao="Pendente",
        data_solicitacao=datetime.now()
    )
    
    try:
        db.add(nova_reserva)
        db.commit()
        db.refresh(nova_reserva)
        return nova_reserva
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao processar a reserva")

@router.get("/user/{id_usuario}", response_model=list[schemas.ReservaResponse])
def listar_minhas_reservas(id_usuario: int, db: Session = Depends(database.get_db)):
    # Retorna todas as reservas que o usuário solicitou como passageiro
    return db.query(models.Reserva).filter(models.Reserva.id_passageiro == id_usuario).all()