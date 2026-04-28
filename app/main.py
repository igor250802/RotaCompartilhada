from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, schemas
from .routers import users, rides, history, vehicles, reservations # Adicionado reservations

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Rota Compartilhada API",
    version="1.1.0"
)

# Configuração de CORS para comunicação com o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTA DE LOGIN (Correção do erro 404)
@app.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == credentials.email).first()
    if not user or user.senha != credentials.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    return user

# Registro das Rotas
app.include_router(users.router)
app.include_router(rides.router)
app.include_router(history.router)
app.include_router(vehicles.router)
app.include_router(reservations.router) # Nova rota integrada

# Montagem de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"status": "API Online", "docs": "/docs"}