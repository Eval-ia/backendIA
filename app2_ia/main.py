from fastapi import FastAPI
from app2_ia.routes import evaluation
from app2_ia.routes import convert

app = FastAPI(title="Evaluación IA con CSV")

app.include_router(evaluation.router)
app.include_router(convert.router)

