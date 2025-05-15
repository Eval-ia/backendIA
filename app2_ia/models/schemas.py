from pydantic import BaseModel
from typing import List, Optional

class CandidatoCrudo(BaseModel):
    candidato_id: str
    puesto: str
    fortalezas: str
    debilidades: str
    valoracion_gpt: str

class CandidatoProcesado(BaseModel):
    candidato_id: str
    puesto: str
    fortalezas: str
    debilidades: str
    valoracion_gpt: str
    texto_limpio: str
    embedding: List[float]
    modelo_embedding: Optional[str] = None
    timestamp: Optional[str] = None

class EmbeddingCandidato(BaseModel):
    candidato_id: str
    embedding: List[float]

class ResultadoCarga(BaseModel):
    validados: int
    descartados: int
    datos: List[CandidatoCrudo]

class ResultadoRanking(BaseModel):
    candidato_id: str
    similitud: float
    ranking: int



