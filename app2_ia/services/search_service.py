import logging
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector, cosine_distance

from app2_ia.services.vector_db import SessionLocal, EmbeddingCandidato
from app2_ia.services.embedding import generar_embedding
from app2_ia.utils.limpieza import limpiar_texto_para_embedding
from app2_ia.models.schemas import ResultadoRanking

logger = logging.getLogger(__name__)

class SearchService:
    """
    Servicio para buscar candidatos similares a un perfil ideal.
    
    Este servicio permite:
    1. Generar un embedding para un perfil ideal
    2. Buscar candidatos similares en la base de datos usando pgvector
    3. Devolver un ranking ordenado por similitud
    """
    
    def search_similar_candidates(
        self, 
        puesto: str, 
        descripcion: str, 
        limit: int = 10,
        filter_by_puesto: bool = True
    ) -> List[ResultadoRanking]:
        """
        Busca candidatos similares a un perfil ideal.
        
        Args:
            puesto: Nombre del puesto para el perfil ideal
            descripcion: Descripción textual del perfil ideal
            limit: Número máximo de resultados a devolver
            filter_by_puesto: Si es True, filtra candidatos solo del mismo puesto
            
        Returns:
            Lista de ResultadoRanking ordenada por similitud descendente
        """
        # 1. Preprocesamiento del texto
        texto_limpio = limpiar_texto_para_embedding(descripcion)
        logger.info(f"Texto limpio para búsqueda de perfil ideal: {texto_limpio[:50]}...")
        
        # 2. Generación del embedding
        embedding_ideal = generar_embedding(texto_limpio)
        logger.info(f"Embedding generado para perfil ideal de puesto: {puesto}")
        
        # 3. Búsqueda en la base de datos
        resultados = self._search_db(puesto, embedding_ideal, limit, filter_by_puesto)
        logger.info(f"Búsqueda completada. Encontrados {len(resultados)} candidatos similares.")
        
        return resultados
    
    def _search_db(
        self, 
        puesto: str, 
        embedding_ideal: List[float], 
        limit: int,
        filter_by_puesto: bool
    ) -> List[ResultadoRanking]:
        """
        Ejecuta la búsqueda en la base de datos usando pgvector.
        
        Args:
            puesto: Puesto para filtrar (si filter_by_puesto es True)
            embedding_ideal: Vector para comparar similitud
            limit: Número máximo de resultados
            filter_by_puesto: Si es True, filtra por puesto
            
        Returns:
            Lista de ResultadoRanking con los candidatos más similares
        """
        # Crear una sesión
        session = SessionLocal()
        try:
            # Preparar la consulta base
            query = session.query(
                EmbeddingCandidato.candidato_id,
                EmbeddingCandidato.puesto,
                # Calcular similitud como 1 - distancia coseno (para convertir distancia a similitud)
                (1 - cosine_distance(EmbeddingCandidato.embedding, embedding_ideal)).label("similitud")
            )
            
            # Filtrar por puesto si es necesario
            if filter_by_puesto:
                query = query.filter(EmbeddingCandidato.puesto == puesto)
                
            # Ordenar por similitud descendente y limitar resultados
            results = query.order_by(desc("similitud")).limit(limit).all()
            
            # Convertir resultados a schema ResultadoRanking
            ranking = []
            for idx, (candidato_id, puesto_candidato, similitud) in enumerate(results, start=1):
                # Redondear similitud a 4 decimales para consistencia con RankingService
                similitud_rounded = round(float(similitud), 4) 
                
                ranking.append(
                    ResultadoRanking(
                        candidato_id=str(candidato_id),
                        similitud=similitud_rounded,
                        ranking=idx
                    )
                )
                logger.debug(
                    f"Candidato {candidato_id} (puesto: {puesto_candidato}) - "
                    f"Similitud: {similitud_rounded:.4f} - Ranking: {idx}"
                )
                
            return ranking
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error en búsqueda vectorial: {e}")
            raise
        finally:
            session.close()
            
    def search_by_existing_embedding(
        self, 
        embedding: List[float], 
        puesto: Optional[str] = None,
        limit: int = 10
    ) -> List[ResultadoRanking]:
        """
        Busca candidatos similares a un embedding ya existente.
        
        Args:
            embedding: Vector de embedding para comparar
            puesto: Si se proporciona, filtra por puesto
            limit: Número máximo de resultados
            
        Returns:
            Lista de ResultadoRanking ordenada por similitud descendente
        """
        return self._search_db(
            puesto=puesto,
            embedding_ideal=embedding, 
            limit=limit,
            filter_by_puesto=puesto is not None
        )