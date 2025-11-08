from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.v1.health import router as health_router
from app.core.logging_config import setup_logging
from app.core.middleware import CorrelationIdMiddleware

import os
import logging

# Inicializa logging
setup_logging()
logger = logging.getLogger("app")

# ============================================================
# Carregando variáveis de ambiente do .env
# ============================================================

load_dotenv()  # Agora o .env será carregado automaticamente

# Configurações do Servidor (via variáveis de ambiente)
APP_NAME = os.getenv("APP_NAME", "FAST Server - Serviços Odontológicos em Análise de Radiografia")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Serviço para análise de radiografias panorâmicas")
DEFAULT_PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")

# ============================================================
# Logging Estruturado
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Inicializando o servidor FAST API...")

# ============================================================
# Instância do FastAPI e Middlewares
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Rotas
# ============================================================


@app.middleware("http")
async def log_requests(request: Request, call_next):
    correlation_id = request.state.correlation_id
    logger.info(f"[{correlation_id}] -> Request: {request.method} {request.url.path}")

    response = await call_next(request)

    logger.info(f"[{correlation_id}] <- Response status: {response.status_code}")
    return response


@app.get("/", summary="Health check")
async def root():
    """Rota de verificação do funcionamento do servidor"""
    logger.info("Health Check solicitado")
    return {"status": "Ok", "service": "Servidor em funcionamento"}

# ============================================================
# Execução Local
# ============================================================
if __name__ == "__main__":
    import uvicorn
    logger.info(f"Iniciando servidor na porta {DEFAULT_PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_PORT, reload=True)