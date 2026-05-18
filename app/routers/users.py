from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/users", tags=["Usuários"])


# ── CREATE ──────────────────────────────────────────────
@router.post("/", response_model=schemas.UserResponse)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """RF01 — Cadastro de novo usuário."""
    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    novo_usuario = models.Usuario(
        nome=user.nome,
        email=user.email,
        senha=user.senha,
        telefone=user.telefone
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


# ── LOGIN ────────────────────────────────────────────────
@router.post("/login")
def login(dados: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """RF02 — Autenticação de usuário."""
    user = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not user or user.senha != dados.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    return {
        "id_usuario": user.id_usuario,
        "nome": user.nome,
        "email": user.email,
        "telefone": user.telefone
    }


# ── READ ─────────────────────────────────────────────────
@router.get("/{user_id}", response_model=schemas.UserResponse)
def buscar_usuario(user_id: int, db: Session = Depends(database.get_db)):
    """Retorna os dados de um usuário pelo ID."""
    user = db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user


# ── UPDATE ───────────────────────────────────────────────
@router.put("/{user_id}", response_model=schemas.UserResponse)
def atualizar_usuario(user_id: int, dados: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    """Atualiza nome, telefone e/ou senha do usuário. Apenas os campos enviados são alterados."""
    user = db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if dados.nome is not None:
        user.nome = dados.nome
    if dados.telefone is not None:
        user.telefone = dados.telefone
    if dados.senha is not None:
        if len(dados.senha) < 6:
            raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 6 caracteres.")
        user.senha = dados.senha

    db.commit()
    db.refresh(user)
    return user


# ── DELETE ───────────────────────────────────────────────
@router.delete("/{user_id}")
def excluir_usuario(user_id: int, db: Session = Depends(database.get_db)):
    """Exclui a conta do usuário e todos os dados vinculados (CASCADE no banco)."""
    user = db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    db.delete(user)
    db.commit()
    return {"message": "Conta excluída com sucesso."}