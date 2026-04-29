from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservas"])

@router.post("/", response_model=schemas.ReservaResponse)
def solicitar_reserva(obj_in: schemas.ReservaCreate, db: Session = Depends(database.get_db)):
    viagem = db.query(models.Viagem).filter(models.Viagem.id_viagem == obj_in.id_viagem).first()
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    
    if viagem.vagas_totais <= 0:
        raise HTTPException(status_code=400, detail="Não há vagas disponíveis")

    nova_reserva = models.Reserva(
        id_viagem=obj_in.id_viagem,
        id_passageiro=obj_in.id_passageiro,
        id_parada_embarque=obj_in.id_parada_embarque,
        id_parada_desembarque=obj_in.id_parada_desembarque,
        quantidade_bagagem=obj_in.quantidade_bagagem,
        status_solicitacao="Pendente", # RF07: Inicia como pendente
        data_solicitacao=datetime.now()
    )
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva

# NOVA ROTA: Aceitar ou Recusar Reserva (RF07)
@router.put("/{id_reserva}/status")
def atualizar_status_reserva(id_reserva: int, status_update: schemas.ReservaUpdateStatus, db: Session = Depends(database.get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id_reserva == id_reserva).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    viagem = db.query(models.Viagem).filter(models.Viagem.id_viagem == reserva.id_viagem).first()

    if status_update.status_solicitacao == "Aceita":
        if viagem.vagas_totais <= 0:
            raise HTTPException(status_code=400, detail="Não há mais vagas nesta viagem")
        viagem.vagas_totais -= 1 # Diminui vaga se aceitar
    
    reserva.status_solicitacao = status_update.status_solicitacao
    db.commit()
    return {"message": f"Reserva {status_update.status_solicitacao} com sucesso"}

# NOVA ROTA: Listar solicitações recebidas pelo motorista
@router.get("/driver/{id_motorista}")
def listar_solicitacoes_para_motorista(id_motorista: int, db: Session = Depends(database.get_db)):
    return db.query(models.Reserva).join(models.Viagem).filter(models.Viagem.id_motorista == id_motorista).all()