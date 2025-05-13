from fastapi import APIRouter, UploadFile, File, HTTPException
from app2_ia.models.schemas import EvaluacionResponse, RankingResponse, Candidato
#from app2_ia.services.ranking import obtener_ranking_por_puesto


# Creamos el router para agrupar endpoints relacionados
router = APIRouter()

# Simulamos una base de datos en memoria agrupando candidatos por puesto
evaluaciones_por_puesto = {}

@router.post("/evaluar", response_model=EvaluacionResponse)
async def evaluar_csv(file: UploadFile = File(...)):
    return #await guardar_candidatos_desde_csv(file)

@router.post("/ranking/{puesto}", response_model=RankingResponse)
async def ranking_puesto(puesto: str):
    return  #obtener_ranking_por_puesto(puesto)
