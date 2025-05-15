from fastapi import FastAPI
from app2_ia.routes import ingest_controller

app = FastAPI()
app.include_router(ingest_controller.router)


