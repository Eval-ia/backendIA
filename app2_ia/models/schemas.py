from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CandidatoCrudo(BaseModel):
    candidato_id: int
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
    timestamp: Optional[datetime] = None

class EmbeddingCandidato(BaseModel):
    candidato_id: str
    embedding: List[float]

class ResultadoCarga(BaseModel):
    validados: int
    descartados: int
    datos: List[CandidatoCrudo]
    errores: List[str] = []    # <-- campo nuevo con valor por defecto

    class Config:
        schema_extra = {
            "example": {
                "validados": 5,
                "descartados": 0,
                "datos": [
                    {
                        "candidato_id": "1001",
                        "puesto": "Desarrollador",
                        "fortalezas": "Lógica",
                        "debilidades": "Poco autónomo",
                        "valoracion_gpt": "Buen razonamiento..."
                    }
                ],
                "errores": []
            }
        }

class ResultadoRanking(BaseModel):
    candidato_id: str
    similitud: float
    ranking: int



