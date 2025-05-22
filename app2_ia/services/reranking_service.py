"""Servicio para refinar el ranking inicial usando un modelo de ML (XGBoost)."""

import logging
from typing import List
import joblib  # pip install joblib
import numpy as np
import xgboost as xgb
from app2_ia.models.schemas import ResultadoRanking

logger = logging.getLogger(__name__)

class RerankingService:
    """
    Servicio para refinar el ranking inicial usando un modelo de ML (XGBoost).
    """

    def __init__(self, model_path: str):
        """
        Carga el modelo de XGBoost previamente entrenado.
        :param model_path: ruta al archivo .joblib del modelo (Booster o sklearn).
        """
        try:
            self.model = joblib.load(model_path)
            logger.info(f"RerankingService cargó modelo de {model_path}")
        except Exception as e:
            logger.error(f"No se pudo cargar el modelo de reranking: {e}")
            raise

    def predict(self, items: List[ResultadoRanking]) -> List[ResultadoRanking]:
        """
        Ajusta el ranking inicial generando un adjusted_score y reordenando.
        :param items: lista de ResultadoRanking (ya con cluster_id y similitud).
        :return: lista de ResultadoRanking con adjusted_score y ranking re-asignado.
        """
        if not items:
            return []

        # 1) Construir matriz de features X
        X = np.array([[r.similitud, r.cluster_id or 0] for r in items])

        # 2) Predecir adjusted_scores
        if isinstance(self.model, xgb.core.Booster):
            dmat = xgb.DMatrix(X)
            scores = self.model.predict(dmat)
        else:
            scores = self.model.predict(X)

        # 3) Asignar adjusted_score y reordenar
        for r, sc in zip(items, scores):
            r.adjusted_score = float(sc)
        items.sort(key=lambda r: r.adjusted_score, reverse=True)

        # 4) Reasignar ranking secuencial
        for idx, r in enumerate(items, start=1):
            r.ranking = idx

        logger.info("Reranking completado correctamente")
        return items
