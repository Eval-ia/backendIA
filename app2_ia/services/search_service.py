# app2_ia/services/search_service.py

import logging
from typing import List, Optional

from app2_ia.utils.limpieza import limpiar_texto_para_embedding
from app2_ia.services.embedding import generar_embedding
from app2_ia.services.vector_db import SessionLocal, EmbeddingCandidato as DBEmbeddingCandidato
from app2_ia.models.schemas import (
    ResultadoRanking,
    EmbeddingCandidato as EmbeddingDTO,
    ClusterAssignment
)
from app2_ia.services.clustering_service import ClusteringService

logger = logging.getLogger(__name__)

def buscar_candidatos_similares(puesto: Optional[str], descripcion: str) -> List[ResultadoRanking]:
    """
    Busca candidatos similares a una descripción de perfil.
    
    Pasos:
    1. Limpia el texto de la descripción
    2. Genera un embedding del texto limpio
    3. Busca en la BD vectorial los candidatos más similares
    4. Realiza clustering y devuelve lista enriquecida
    
    Returns:
        Lista de ResultadoRanking con los candidatos más similares
    """
    # 1. Limpieza del texto
    logger.info(
        f"Procesando búsqueda para descripción"
        + (f" y puesto: {puesto}" if puesto else "")
    )
    texto_limpio = limpiar_texto_para_embedding(descripcion)
    logger.debug(f"Texto limpio: {texto_limpio[:50]}...")

    # 2. Generación del embedding
    embedding_busqueda = generar_embedding(texto_limpio)
    logger.debug("Embedding generado para la búsqueda")

    # 3. Consulta en la base de datos
    session = SessionLocal()
    try:
        resultados = []
        if puesto:
            query = (
                session.query(
                    DBEmbeddingCandidato,
                    DBEmbeddingCandidato.embedding.cosine_distance(embedding_busqueda).label("distancia")
                )
                .filter(DBEmbeddingCandidato.puesto == puesto)
                .order_by("distancia")
                .limit(10)
                .all()
            )
            resultados = query

            if not resultados:
                logger.info(
                    f"No se encontraron resultados para el puesto '{puesto}'. "
                    "Buscando en todos los puestos."
                )

        if not puesto or not resultados:
            query = (
                session.query(
                    DBEmbeddingCandidato,
                    DBEmbeddingCandidato.embedding.cosine_distance(embedding_busqueda).label("distancia")
                )
                .order_by("distancia")
                .limit(10)
                .all()
            )
            resultados = query

        # 4. Preparar objetos para clustering
        candidatos_para_clustering: List[EmbeddingDTO] = []
        for candidato, distancia in resultados:
            vector = getattr(candidato, "embedding", None)
            if vector is None:
                logger.warning(
                    f"No se encontró 'embedding' para el candidato {candidato.candidato_id}"
                )
                continue
            candidatos_para_clustering.append(
                EmbeddingDTO(
                    candidato_id=str(candidato.candidato_id),
                    embedding=vector.to_list() if hasattr(vector, "to_list") else list(vector)
                )
            )

        # 5. Ejecutar clustering KMeans (maneja n_samples < n_clusters)
        clustering_service = ClusteringService(n_clusters=3)
        asignaciones: List[ClusterAssignment] = clustering_service.fit_predict(
            candidatos_para_clustering
        )
        mapa_clusters = {a.candidato_id: a.cluster_id for a in asignaciones}

        # 6. Construcción del ranking enriquecido con cluster_id
        ranking_resultados: List[ResultadoRanking] = []
        for i, (candidato, distancia) in enumerate(resultados):
            similitud = 1 - distancia if distancia <= 1 else 0
            cid = str(candidato.candidato_id)

            ranking = ResultadoRanking(
                candidato_id=cid,
                similitud=round(similitud, 4),
                ranking=i + 1,
                puesto=candidato.puesto,
                cluster_id=mapa_clusters.get(cid)
            )
            ranking_resultados.append(ranking)

        logger.info(f"Búsqueda completada: {len(ranking_resultados)} resultados")
        return ranking_resultados

    except Exception as e:
        logger.error(f"Error en búsqueda vectorial: {e}")
        raise
    finally:
        session.close()
