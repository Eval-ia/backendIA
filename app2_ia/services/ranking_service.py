from typing import List
from models.contracts import EmbeddingCandidato, ResultadoRanking
from services.similarity import SimilarityCalculator

class RankingService:
    """
    Servicio para calcular el ranking de candidatos en base a la similitud
    con un embedding de referencia.
    """

    def __init__(self, similarity: SimilarityCalculator):
        self.similarity = similarity

    def rank(
        self,
        embedding_referencia: List[float],
        candidatos: List[EmbeddingCandidato]
    ) -> List[ResultadoRanking]:
        """
        Devuelve la lista de candidatos ordenada de mayor a menor similitud.
        """
        # 1. Calcular similitud
        scored = []
        for cand in candidatos:
            score = self.similarity.calculate(embedding_referencia, cand.embedding)
            scored.append((cand.candidato_id, score))

        # 2. Ordenar descendente
        scored.sort(key=lambda x: x[1], reverse=True)

        # 3. Generar ResultadoRanking con ranking secuencial
        ranking = []
        for idx, (cid, sim) in enumerate(scored, start=1):
            ranking.append(ResultadoRanking(
                candidato_id=cid,
                similitud=round(sim, 4),
                ranking=idx
            ))

        return ranking
