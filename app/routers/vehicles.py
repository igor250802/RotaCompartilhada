from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List

router = APIRouter(prefix="/vehicles", tags=["Veículos"])

@router.post("/", response_model=schemas.VeiculoResponse)
def cadastrar_veiculo(veiculo: schemas.VeiculoCreate, db: Session = Depends(database.get_db)):
    novo = models.Veiculo(**veiculo.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/user/{user_id}", response_model=List[schemas.VeiculoResponse])
def listar_veiculos(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Veiculo).filter(models.Veiculo.id_proprietario == user_id).all()

@router.delete("/{vehicle_id}")
def excluir_veiculo(vehicle_id: int, db: Session = Depends(database.get_db)):
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == vehicle_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    db.delete(veiculo)
    db.commit()
    return {"status": "sucesso"}