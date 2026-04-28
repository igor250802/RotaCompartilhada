from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List

router = APIRouter(prefix="/rides", tags=["Caronas"])

@router.post("/", response_model=schemas.ViagemResponse)
def oferecer_carona(obj_in: schemas.ViagemCreate, db: Session = Depends(database.get_db)):
    # 1. Cria a Viagem principal
    nova_viagem = models.Viagem(
        id_motorista=obj_in.id_motorista,
        id_veiculo=obj_in.id_veiculo,
        data_hora=obj_in.data_hora,
        vagas_totais=obj_in.vagas_totais,
        status_viagem="Aberta"
    )
    db.add(nova_viagem)
    db.flush()  # Gera o ID da viagem para as paradas

    # 2. Adiciona as cidades do itinerário
    for p in obj_in.itinerario:
        nova_parada = models.Parada(
            id_viagem=nova_viagem.id_viagem,
            cidade=p.cidade,
            ordem_parada=p.ordem_parada
        )
        db.add(nova_parada)
    
    db.commit()
    db.refresh(nova_viagem)
    return nova_viagem

@router.get("/search/{destino}", response_model=List[schemas.ViagemResponse])
def buscar_caronas(destino: str, db: Session = Depends(database.get_db)):
    # Busca viagens que possuem a cidade no itinerário e têm vagas
    return db.query(models.Viagem).join(models.Parada).filter(
        models.Parada.cidade.ilike(f"%{destino}%"),
        models.Viagem.status_viagem == "Aberta",
        models.Viagem.vagas_totais > 0
    ).distinct().all()