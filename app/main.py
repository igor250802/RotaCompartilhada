from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # Adicionado para servir a home
from sqlalchemy.orm import Session
import os
from . import models, database, schemas
from .routers import users, rides, history, vehicles, reservations

# Cria tabelas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Rota Sul API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTA PARA ACESSAR A HOME DIRETAMENTE
@app.get("/home")
def get_home():
    # Retorna o index.html que está dentro da pasta static
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == credentials.email).first()
    if not user or user.senha != credentials.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    return user

app.include_router(users.router)
app.include_router(rides.router)
app.include_router(history.router)
app.include_router(vehicles.router)
app.include_router(reservations.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"status": "Online", "acesso_home": "/home"}