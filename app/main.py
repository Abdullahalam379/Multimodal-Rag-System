from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api.routes import router


app = FastAPI(
    title="Multimodal RAG System",
    description="A simple multimodal RAG system using OpenAI, OCR, and ChromaDB.",
    version="1.0.0",
)
metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app,
)
app.include_router(router)