from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app2_ia.services.search_service import buscar_candidatos_similares
from app2_ia.models.schemas import ResultadoRanking

router = APIRouter()

class BusquedaPerfil(BaseModel):
    puesto: str
    descripcion: str

@router.post(
    "/buscar_similares",
    response_model=List[ResultadoRanking],
    summary="Busca candidatos similares a una descripción de perfil"
)
async def buscar_similares(busqueda: BusquedaPerfil):
    try:
        resultados = buscar_candidatos_similares(
            busqueda.puesto, 
            busqueda.descripcion
        )
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {e}")