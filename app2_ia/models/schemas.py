from pydantic import BaseModel
from typing import List

# Modelo de respuesta al subir el CSV
class EvaluacionResponse(BaseModel):
    mensaje: str
    candidatos_procesados: int

# Modelo que representa a un candidato individual
class Candidato(BaseModel):
    nombre: str
    score: float
    fortalezas: str
    debilidades: str

# Modelo de respuesta al pedir el ranking de un puesto
class RankingResponse(BaseModel):
    puesto: str
    candidatos: List[Candidato]
