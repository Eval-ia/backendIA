# app2_ia/scripts/train_reranking.py

import json
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Rutas de datos y modelo
TRAIN_JSON = os.path.join("data", "reranking_train.json")
MODEL_PATH = os.path.join("models", "reranker.joblib")

def main():
    # 1) Carga de datos
    if not os.path.isfile(TRAIN_JSON):
        raise FileNotFoundError(f"No existe el archivo de entrenamiento: {TRAIN_JSON}")
    with open(TRAIN_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # 2) Construcción de X e y
    X, y = [], []
    for item in raw:
        feats = [
            item["similitud"],
            item.get("cluster_id", 0),
        ]
        X.append(feats)
        y.append(item["label_score"])
    X = np.array(X)
    y = np.array(y)

    # 3) División en train/validation
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4) Construcción de DMatrix para XGBoost
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval   = xgb.DMatrix(X_val,   label=y_val)

    # 5) Definición de parámetros
    params = {
        "objective": "reg:squarederror",
        "learning_rate": 0.1,
        "seed": 42
    }

    # 6) Entrenamiento con early stopping
    bst = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dval, "validation")],
        early_stopping_rounds=10,
        verbose_eval=True
    )

    # 7) Guardar el Booster entrenado
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(bst, MODEL_PATH)
    print(f"✅ Booster entrenado y guardado en {MODEL_PATH}")

if __name__ == "__main__":
    main()
