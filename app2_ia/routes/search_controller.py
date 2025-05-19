from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app2_ia.services.search_service import SearchService
from app2_ia.models.schemas import ResultadoRanking

router = APIRouter()

# Definimos un modelo para la petición
class PerfilIdealRequest(BaseModel):
    puesto: str
    descripcion: str
    limit: Optional[int] = 10
    filter_by_puesto: Optional[bool] = True
    
    class Config:
        schema_extra = {
            "example": {
                "puesto": "Desarrollador",
                "descripcion": "Buscamos un profesional con fuertes habilidades técnicas, capacidad para resolver problemas complejos y trabajar en equipo. Idealmente con experiencia en desarrollo web y conocimientos de bases de datos.",
                "limit": 5,
                "filter_by_puesto": True
            }
        }

@router.post(
    "/buscar_candidatos_similares",
    response_model=List[ResultadoRanking],
    summary="Busca candidatos similares a un perfil ideal"
)
async def buscar_candidatos_similares(request: PerfilIdealRequest):
    """
    Busca candidatos similares a un perfil ideal.
    
    Esta ruta toma una descripción de perfil ideal, la convierte en embedding,
    y busca candidatos similares en la base de datos vectorial.
    
    - *puesto*: Puesto para el que se busca candidatos
    - *descripcion*: Descripción textual del perfil ideal
    - *limit*: Número máximo de resultados (por defecto 10)
    - *filter_by_puesto*: Si es True, solo busca candidatos del mismo puesto
    
    Retorna una lista ordenada de candidatos por similitud descendente.
    """
    try:
        search_service = SearchService()
        resultados = search_service.search_similar_candidates(
            puesto=request.puesto,
            descripcion=request.descripcion,
            limit=request.limit,
            filter_by_puesto=request.filter_by_puesto
        )
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")


# Endpoint adicional para búsqueda por embedding existente
class EmbeddingSearchRequest(BaseModel):
    embedding: List[float]
    puesto: Optional[str] = None
    limit: Optional[int] = 10
    
    class Config:
        schema_extra = {
            "example": {
                "embedding": [0.1, 0.2, 0.3, 0.4, 0.5],  # Recuerda que necesitas 1536 valores
                "puesto": "Desarrollador",
                "limit": 5
            }
        }

@router.post(
    "/buscar_por_embedding",
    response_model=List[ResultadoRanking],
    summary="Busca candidatos similares a un embedding existente"
)
async def buscar_por_embedding(request: EmbeddingSearchRequest):
    """
    Busca candidatos similares a un embedding existente.
    
    Esta ruta permite buscar candidatos usando directamente un vector de embedding,
    sin necesidad de procesar texto. Útil para comparar con embeddings ya generados.
    
    - *embedding*: Vector de embedding (1536 dimensiones)
    - *puesto*: Si se proporciona, filtra por puesto
    - *limit*: Número máximo de resultados (por defecto 10)
    
    Retorna una lista ordenada de candidatos por similitud descendente.
    """
    try:
        # Validación básica de dimensiones del embedding
        if len(request.embedding) != 1536:
            raise ValueError(f"El embedding debe tener 1536 dimensiones, pero tiene {len(request.embedding)}")
            
        search_service = SearchService()
        resultados = search_service.search_by_existing_embedding(
            embedding=request.embedding,
            puesto=request.puesto,
            limit=request.limit
        )
        return resultados
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")