from abc import ABC, abstractmethod
from typing import List
from math import sqrt


class SimilarityCalculator(ABC):
    """
    Interfaz para calcular la similitud entre dos vectores.
    """

    @abstractmethod
    def calculate(self, v1: List[float], v2: List[float]) -> float:
        """
        Calcula y devuelve un valor de similitud entre 0.0 y 1.0
        para los vectores v1 y v2.
        """
        pass


class CosineSimilarity(SimilarityCalculator):
    """
    Implementación de la métrica de similitud coseno.
    """

    def calculate(self, v1: List[float], v2: List[float]) -> float:
        """
        Calcula la similitud coseno:

            sim(v1, v2) = (v1 · v2) / (||v1|| * ||v2||)

        :raises ValueError: si las longitudes difieren
        :return: similitud coseno o 0.0 si alguna norma es cero
        """
        if len(v1) != len(v2):
            raise ValueError("Los vectores deben tener la misma longitud")

        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0
        for a, b in zip(v1, v2):
            dot_product += a * b
            norm1 += a * a
            norm2 += b * b

        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0

        return dot_product / (sqrt(norm1) * sqrt(norm2))
