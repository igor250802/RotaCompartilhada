from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("/", response_model=schemas.UserResponse)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo_usuario = models.Usuario(nome=user.nome, email=user.email, senha=user.senha, telefone=user.telefone)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login")
def login(dados: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not user or user.senha != dados.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"id_usuario": user.id_usuario, "nome": user.nome, "email": user.email, "telefone": user.telefone}

@router.put("/{user_id}", response_model=schemas.UserResponse)
def atualizar_usuario(user_id: int, dados: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Não encontrado")
    user.nome = dados.nome
    user.telefone = dados.telefone
    db.commit()
    db.refresh(user)
    return user