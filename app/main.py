from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users

# Cria as tabelas no MySQL automaticamente se elas não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rota Compartilhada API")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API Rota Compartilhada rodando com MySQL!"}