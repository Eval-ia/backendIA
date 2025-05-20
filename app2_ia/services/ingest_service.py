import os
import logging
import pandas as pd
from datetime import datetime
from typing import Tuple, List

from app2_ia.utils.validacion import validar_filas
from app2_ia.utils.limpieza import limpiar_texto_para_embedding
from app2_ia.services.embedding import generar_embedding
from app2_ia.models.schemas import CandidatoCrudo, ResultadoCarga
from app2_ia.services.vector_db import insertar_en_vectordb, existe_candidato


logger = logging.getLogger(__name__)

def cargar_y_validar_csv(file) -> Tuple[List[CandidatoCrudo], List[str]]:
    """
    Lee un CSV desde UploadFile, valida filas y devuelve:
      - Lista de CandidatoCrudo ya tipados.
      - Lista de errores (strings) si los hay.
    """
    # Leemos el CSV
    df = pd.read_csv(file.file)

    # Validamos con nuestra función; resulta en dos listas de dicts y errores
    filas_validas, errores = validar_filas(df)

    # Convertimos cada fila válida en un objeto Pydantic
    candidatos: List[CandidatoCrudo] = []
    for fila in filas_validas:
        try:
            candidato = CandidatoCrudo(
                candidato_id=fila["candidato_id"],
                puesto=fila["puesto"],
                fortalezas=fila["fortalezas"],
                debilidades=fila["debilidades"],
                valoracion_gpt=fila["valoracion_gpt"]
            )
            candidatos.append(candidato)
        except Exception as e:
            # Capturamos cualquier error inesperado de Pydantic
            error_msg = f"Error al parsear fila {fila}: {e}"
            logger.error(error_msg)
            errores.append(error_msg)

    # Si hubo errores, los volcamos a un archivo de log
    if errores:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_log = os.path.join("logs", f"errores_{timestamp}.log")
        with open(ruta_log, "w", encoding="utf-8") as f:
            for err in errores:
                f.write(err + "\n")
        logger.info(f"Log de errores guardado en {ruta_log}")

    return candidatos, errores


def procesar_y_guardar_candidatos(candidatos: List[CandidatoCrudo]) -> ResultadoCarga:
    """
    Recorre cada candidato:
      1. Limpia su texto con SpaCy.
      2. Genera embedding.
      3. Inserta en la BD vectorial (pgvector).
    Devuelve un ResultadoCarga con totales y datos procesados.
    """
    insertados = 0
    descartados = 0
    duplicados: List[str] = []
    datos_procesados: List[dict] = []
    for candidato in candidatos:
        if existe_candidato(int(candidato.candidato_id)):
            msg = f"Candidato duplicado (ID: {candidato.candidato_id})"
            logger.warning(msg)
            duplicados.append(str(candidato.candidato_id))
            descartados += 1
            continue
        
        # 1. Preprocesamiento
        texto_limpio = limpiar_texto_para_embedding(candidato.valoracion_gpt)
        logger.debug(f"Texto limpio para {candidato.candidato_id}: {texto_limpio[:50]}...")

        # 2. Generación de embedding
        embedding = generar_embedding(texto_limpio)
        logger.debug(f"Embedding generado para {candidato.candidato_id}")

        # 3. Preparar objeto para BD vectorial
        objeto_final = {
            "candidato_id": candidato.candidato_id,
            "puesto": candidato.puesto,
            "embedding": embedding,
            "metadata": {
                "fortalezas": candidato.fortalezas,
                "debilidades": candidato.debilidades,
                "fuente": "entrevista GPT"
            }
        }

        # 4. Inserción en la BD
        insertar_en_vectordb(objeto_final)
        insertados += 1
        datos_procesados.append(candidato.dict())  # Solo los que se insertan
        logger.info(f"Candidato {candidato.candidato_id} insertado en VectorDB")


    return ResultadoCarga(
        validados=insertados,
        descartados=0,
        datos=datos_procesados,
        duplicados= duplicados
    )
