from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import users, rides, history, vehicles # 1. Adicionado 'vehicles'

# Cria as tabelas no MySQL automaticamente ao iniciar o servidor
# Isso garante que a tabela de Veículos e as outras existam no seu banco
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Rota Compartilhada API",
    description="Backend para sistema de caronas universitárias",
    version="1.0.0"
)

# 2. Configuração de CORS
# Permite que o seu navegador (Front-end) se comunique com o Python (Back-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Montagem da pasta de arquivos estáticos
# Essencial para que http://127.0.0.1:8000/static/index.html funcione
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Registro das Rotas (Endpoints)
# Certifique-se de que cada arquivo .py existe dentro da pasta 'app/routers/'
app.include_router(users.router)
app.include_router(rides.router)
app.include_router(history.router)
app.include_router(vehicles.router) # 5. Nova rota de veículos registrada

# Rota raiz para verificação rápida de status
@app.get("/")
def read_root():
    return {
        "status": "API Online",
        "projeto": "Rota Compartilhada",
        "docs": "Acesse /docs para testar as rotas manualmente"
    }