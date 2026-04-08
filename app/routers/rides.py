from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func
from .. import models, schemas, database
from datetime import date

router = APIRouter(prefix="/rides", tags=["Viagens e Reservas"])

# --- ROTAS DE VIAGEM ---

@router.post("/", response_model=schemas.ViagemResponse)
def criar_viagem(obj_in: schemas.ViagemCreate, db: Session = Depends(database.get_db)):
    """
    RF03: Permite que o motorista cadastre uma nova viagem com seu itinerário completo.
    """
    # 1. Instanciar a viagem principal
    nova_viagem = models.Viagem(
        id_motorista=obj_in.id_motorista,
        id_veiculo=obj_in.id_veiculo,
        data_hora=obj_in.data_hora,
        vagas_totais=obj_in.vagas_totais,
        status_viagem="Aberta"
    )
    db.add(nova_viagem)
    db.flush()  # Gera o ID da viagem para vincular as paradas

    # 2. Adicionar as paradas do itinerário conforme a ordem informada
    for p in obj_in.itinerario:
        parada = models.Parada(
            id_viagem=nova_viagem.id_viagem,
            cidade=p.cidade,
            ordem_parada=p.ordem_parada
        )
        db.add(parada)
    
    db.commit()
    db.refresh(nova_viagem)
    return nova_viagem

@router.get("/search", response_model=list[schemas.ViagemResponse])
def buscar_caronas(
    origem: str = Query(..., description="Cidade de partida"),
    destino: str = Query(..., description="Cidade de chegada"),
    data: date = Query(None, description="Data da viagem (AAAA-MM-DD)"),
    db: Session = Depends(database.get_db)
):
    """
    RF05: Busca viagens onde a origem e o destino existam no itinerário e a origem venha antes.
    """
    p_origem = aliased(models.Parada)
    p_destino = aliased(models.Parada)

    query = db.query(models.Viagem).join(
        p_origem, models.Viagem.id_viagem == p_origem.id_viagem
    ).join(
        p_destino, models.Viagem.id_viagem == p_destino.id_viagem
    ).filter(
        p_origem.cidade.ilike(f"%{origem}%"),
        p_destino.cidade.ilike(f"%{destino}%"),
        p_origem.ordem_parada < p_destino.ordem_parada, # Garante o sentido correto
        models.Viagem.status_viagem == "Aberta"
    )

    if data:
        query = query.filter(func.date(models.Viagem.data_hora) == data)

    resultados = query.all()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhuma carona encontrada para este trajeto.")
    
    return resultados

# --- ROTAS DE RESERVA ---

@router.post("/reserve", response_model=schemas.ReservaResponse)
def solicitar_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(database.get_db)):
    """
    RF04 e RF06: Passageiro solicita vaga informando a quantidade de bagagem.
    """
    viagem = db.query(models.Viagem).filter(models.Viagem.id_viagem == reserva.id_viagem).first()
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada.")
    
    if viagem.vagas_totais <= 0:
        raise HTTPException(status_code=400, detail="Não há vagas disponíveis nesta viagem.")

    nova_reserva = models.Reserva(
        id_viagem=reserva.id_viagem,
        id_passageiro=reserva.id_passageiro,
        id_parada_embarque=reserva.id_parada_embarque,
        id_parada_desembarque=reserva.id_parada_desembarque,
        quantidade_bagagem=reserva.quantidade_bagagem, #
        status_solicitacao="Pendente"
    )
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva

@router.patch("/reservas/{id_reserva}/status", response_model=schemas.ReservaResponse)
def alterar_status_reserva(
    id_reserva: int, 
    status_update: schemas.ReservaUpdateStatus, 
    db: Session = Depends(database.get_db)
):
    """
    RF07: Motorista aceita ou recusa a solicitação. Se aceita, abate uma vaga da viagem.
    """
    reserva = db.query(models.Reserva).filter(models.Reserva.id_reserva == id_reserva).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    
    # Atualiza o status conforme definido no Enum
    reserva.status_solicitacao = status_update.status_solicitacao
    
    if status_update.status_solicitacao == "Aceita":
        viagem = db.query(models.Viagem).filter(models.Viagem.id_viagem == reserva.id_viagem).first()
        if viagem.vagas_totais > 0:
            viagem.vagas_totais -= 1
        else:
            raise HTTPException(status_code=400, detail="A viagem lotou antes da aprovação.")

    db.commit()
    db.refresh(reserva)
    return reserva