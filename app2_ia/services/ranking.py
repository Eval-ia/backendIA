from fastapi import HTTPException
from app2_ia.models.schemas import RankingResponse, Candidato

def obtener_ranking_por_puesto(puesto: str) -> RankingResponse:
    """
    puesto_lower = puesto.lower()

    # Buscar el puesto ignorando mayúsculas
    puesto_encontrado = None
    for clave in evaluaciones_por_puesto.keys():
        if clave.lower() == puesto_lower:
            puesto_encontrado = clave
            break

    if not puesto_encontrado:
        raise HTTPException(status_code=404, detail="No hay evaluaciones para este puesto")

    # Ordenamos candidatos por score (descendente)
    candidatos_ordenados = sorted(
        evaluaciones_por_puesto[puesto],
        key=lambda c: c["score"],
        reverse=True
    )
    """
    

    # Convertimos diccionarios a objetos Candidato
    """
    candidatos = [Candidato(**c) for c in candidatos_ordenados]

    return RankingResponse(puesto=puesto, candidatos=candidatos)
    """
    
