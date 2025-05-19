from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app2_ia.routes import ingest_controller, search_controller


app = FastAPI(
    title="Eval-IA Backend",
    description="API para evaluación de candidatos mediante IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  # En producción, limitar a orígenes específicos
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(ingest_controller.router, prefix="/api", tags=["Ingestión"])
app.include_router(search_controller.router, prefix="/api", tags=["Búsqueda"])