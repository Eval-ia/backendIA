import pandas as pd
import os
from datetime import datetime
from app2_ia.utils.validacion import validar_filas
from app2_ia.utils.limpieza import limpiar_texto  
from app2_ia.services.embedding import generar_embedding  
from app2_ia.services.vector_db import insertar_en_vectordb


def cargar_y_validar_csv(file):
    df = pd.read_csv(file.file)
    candidatos_validos, errores = validar_filas(df)

    if errores:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"logs/errores_{timestamp}.log", "w", encoding="utf-8") as f:
            for err in errores:
                f.write(err + "\n")
        print(f"[INFO] Log de errores guardado.")

    return candidatos_validos, errores


def procesar_y_guardar_candidatos(candidatos):
    for candidato in candidatos:
        texto_limpio = limpiar_texto(candidato["valoracion_gpt"])
        embedding = generar_embedding(texto_limpio)

        objeto_final = {
            "candidato_id": candidato["candidato_id"],
            "puesto": candidato["puesto"],
            "embedding": embedding,
            "metadata": {
                "fortalezas": candidato["fortalezas"],
                "debilidades": candidato["debilidades"],
                "fuente": "entrevista GPT"
            }
        }

        insertar_en_vectordb(objeto_final)

