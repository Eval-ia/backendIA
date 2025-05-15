import logging
from abc import ABC, abstractmethod
from typing import List
from math import sqrt

logger = logging.getLogger(__name__)


class SimilarityCalculator(ABC):
    """
    Interfaz para calcular la similitud entre dos vectores.

    Esta interfaz permite definir múltiples estrategias de cálculo
    de similitud que se pueden inyectar en servicios como RankingService.
    Cada implementación debe recibir dos vectores de igual dimensión
    y devolver un valor entre 0.0 (sin similitud) y 1.0 (idénticos).
    """

    @abstractmethod
    def calculate(self, v1: List[float], v2: List[float]) -> float:
        """
        Calcula la similitud entre los vectores v1 y v2.

        Args:
            v1 (List[float]): Primer vector.
            v2 (List[float]): Segundo vector.

        Returns:
            float: Valor de similitud en rango [0.0, 1.0].

        Raises:
            ValueError: Si los vectores no tienen la misma longitud.
        """
        pass


class CosineSimilarity(SimilarityCalculator):
    """
    Implementación de la similitud coseno.

    Calcula la métrica:

        sim(v1, v2) = (v1 · v2) / (||v1|| * ||v2||)

    Se puede inyectar donde se requiera comparar embeddings u
    otros vectores numéricos.
    """

    def calculate(self, v1: List[float], v2: List[float]) -> float:
        """
        Calcula la similitud coseno entre v1 y v2.

        Args:
            v1 (List[float]): Primer vector de características.
            v2 (List[float]): Segundo vector de características.

        Returns:
            float: Similitud coseno en [0.0, 1.0]. Retorna 0.0 si alguna norma es cero.

        Raises:
            ValueError: Si las longitudes de v1 y v2 difieren.
        """
        if len(v1) != len(v2):
            logger.error(
                "Error de longitud: len(v1)=%d, len(v2)=%d", 
                len(v1), len(v2)
            )
            raise ValueError("Los vectores deben tener la misma longitud")

        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0

        for a, b in zip(v1, v2):
            dot_product += a * b
            norm1 += a * a
            norm2 += b * b

        logger.debug(
            "CosineSimilarity cálculo intermedio: dot_product=%.4f, norm1=%.4f, norm2=%.4f",
            dot_product, norm1, norm2
        )

        if norm1 == 0.0 or norm2 == 0.0:
            logger.warning(
                "Una de las normas es cero (norm1=%f, norm2=%f). Devolviendo 0.0.", 
                norm1, norm2
            )
            return 0.0

        similarity = dot_product / (sqrt(norm1) * sqrt(norm2))
        logger.debug("Similitud coseno resultante: %.4f", similarity)
        return similarity
