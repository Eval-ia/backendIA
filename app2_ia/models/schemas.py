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



