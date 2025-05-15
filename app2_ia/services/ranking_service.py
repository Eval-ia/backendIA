import logging
from typing import List
from app2_ia.models.schemas import EmbeddingCandidato, ResultadoRanking
from app2_ia.services.similarity import SimilarityCalculator

logger = logging.getLogger(__name__)


class RankingService:
    """
    Servicio para calcular el ranking de candidatos en base a la similitud
    con un embedding de referencia.

    Esta clase permite inyectar distintas implementaciones de SimilarityCalculator
    para usar diferentes métricas de similitud en el futuro.
    """

    def __init__(self, similarity: SimilarityCalculator):
        """
        Inicializa el servicio con una estrategia de similitud.

        Args:
            similarity (SimilarityCalculator): Estrategia para calcular la similitud.
        """
        self.similarity = similarity
        logger.info("RankingService inicializado con estrategia %s", type(similarity).__name__)

    def rank(
        self,
        embedding_referencia: List[float],
        candidatos: List[EmbeddingCandidato]
    ) -> List[ResultadoRanking]:
        """
        Calcula y devuelve la lista de candidatos ordenada de mayor a menor similitud.

        Args:
            embedding_referencia (List[float]): Embedding del perfil ideal.
            candidatos (List[EmbeddingCandidato]): Lista de candidatos con sus embeddings.

        Returns:
            List[ResultadoRanking]: Lista ordenada donde cada elemento contiene:
                - candidato_id: ID del candidato.
                - similitud: similitud coseno (redondeada a 4 decimales).
                - ranking: posición en el ranking (1 = más similar).
        """
        # 1. Calcular similitud para cada candidato
        scored: List[tuple[str, float]] = []
        for cand in candidatos:
            score = self.similarity.calculate(embedding_referencia, cand.embedding)
            logger.debug("Similitud para candidato %s: %.4f", cand.candidato_id, score)
            scored.append((cand.candidato_id, score))

        # 2. Ordenar descendente por similitud
        scored.sort(key=lambda x: x[1], reverse=True)
        logger.info("Candidatos ordenados por similitud descendente")

        # 3. Generar ResultadoRanking con ranking secuencial
        ranking: List[ResultadoRanking] = []
        for idx, (cid, sim) in enumerate(scored, start=1):
            ranking.append(
                ResultadoRanking(
                    candidato_id=cid,
                    similitud=round(sim, 4),
                    ranking=idx
                )
            )
            logger.debug("Posición %d: candidato %s (similitud=%.4f)", idx, cid, sim)

        logger.info("Ranking completo generado para %d candidatos", len(ranking))
        return ranking
