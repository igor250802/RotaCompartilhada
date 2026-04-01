from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("/", response_model=schemas.UserResponse)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Verifica se e-mail já existe
    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar novo usuário (Dica: Use hash na senha depois!)
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