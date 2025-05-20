# app2_ia/services/search_service.py
import logging
from typing import List
from app2_ia.utils.limpieza import limpiar_texto_para_embedding
from app2_ia.services.embedding import generar_embedding
from app2_ia.services.vector_db import SessionLocal, EmbeddingCandidato
from app2_ia.models.schemas import ResultadoRanking

logger = logging.getLogger(_name_)

def buscar_candidatos_similares(puesto: str, descripcion: str) -> List[ResultadoRanking]:
    """
    Busca candidatos similares a una descripción de perfil.
    
    Pasos:
    1. Limpia el texto de la descripción
    2. Genera un embedding del texto limpio
    3. Busca en la BD vectorial los candidatos más similares
    4. Devuelve lista ordenada de candidatos
    
    Args:
        puesto: Nombre o código del puesto
        descripcion: Texto describiendo el perfil ideal
        
    Returns:
        Lista de ResultadoRanking con los candidatos más similares
    """
    # 1. Limpieza del texto
    logger.info(f"Procesando búsqueda para puesto: {puesto}")
    texto_limpio = limpiar_texto_para_embedding(descripcion)
    logger.debug(f"Texto limpio: {texto_limpio[:50]}...")
    
    # 2. Generación del embedding
    embedding_busqueda = generar_embedding(texto_limpio)
    logger.debug("Embedding generado para la búsqueda")
    
    # 3. Búsqueda en la base de datos
    session = SessionLocal()
    try:
        # Filtrar por puesto si se especifica
        query = session.query(
            EmbeddingCandidato,
            # Utiliza la función de similitud coseno de pgvector
            EmbeddingCandidato.embedding.cosine_distance(embedding_busqueda).label('distancia')
        )
        
        # Filtrar por puesto
        query = query.filter(EmbeddingCandidato.puesto == puesto)
        
        # Ordenar por similitud (menor distancia = mayor similitud)
        resultados = query.order_by('distancia').all()
        
        # 4. Construcción de la respuesta
        ranking_resultados = []
        for i, (candidato, distancia) in enumerate(resultados):
            # Convertir distancia a similitud (1 - distancia)
            similitud = 1 - distancia if distancia <= 1 else 0
            
            # Crear objeto de resultado
            ranking = ResultadoRanking(
                candidato_id=str(candidato.candidato_id),
                similitud=round(similitud, 4),  # Redondear a 4 decimales
                ranking=i + 1  # El ranking empieza en 1
            )
            ranking_resultados.append(ranking)
            
        logger.info(f"Búsqueda completada: {len(ranking_resultados)} resultados")
        return ranking_resultados
        
    except Exception as e:
        logger.error(f"Error en búsqueda vectorial: {e}")
        raise
    finally:
        session.close()