from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="SIAC API",
    description="Sistema Inteligente de Asistencia Clínica con RAG",
    version="1.0.0"
)

app.include_router(router)
