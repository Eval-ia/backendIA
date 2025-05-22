# app2_ia/services/clustering_service.py

import logging
from typing import List
from sklearn.cluster import KMeans
from app2_ia.models.schemas import EmbeddingCandidato, ClusterAssignment

logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self, n_clusters: int = 3):
        """
        Inicializa el servicio de clustering con el número de clústeres deseado.
        :param n_clusters: Número de clústeres para KMeans.
        """
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        logger.info(f"ClusteringService inicializado con KMeans (n_clusters={n_clusters})")

    def fit_predict(self, candidatos: List[EmbeddingCandidato]) -> List[ClusterAssignment]:
        """
        Realiza clustering sobre los embeddings de los candidatos.
        :param candidatos: Lista de EmbeddingCandidato con los embeddings.
        :return: Lista de ClusterAssignment con las asignaciones de clúster.
        """
        n_samples = len(candidatos)
        if n_samples == 0:
            logger.warning("Lista de candidatos vacía. No se realizará clustering.")
            return []

        # Si hay menos muestras que clústeres, asignamos todos al cluster 0
        if n_samples < self.n_clusters:
            logger.warning(
                f"Muestras ({n_samples}) < n_clusters ({self.n_clusters}), "
                "asignando cluster_id=0 a todos"
            )
            return [
                ClusterAssignment(candidato_id=c.candidato_id, cluster_id=0)
                for c in candidatos
            ]

        embeddings = [c.embedding for c in candidatos]
        candidato_ids = [c.candidato_id for c in candidatos]

        logger.debug(f"Aplicando KMeans a {n_samples} embeddings...")
        cluster_ids = self.model.fit_predict(embeddings)

        resultado = [
            ClusterAssignment(candidato_id=cid, cluster_id=int(clid))
            for cid, clid in zip(candidato_ids, cluster_ids)
        ]

        logger.info("Clustering completado. Clusters asignados.")
        return resultado
