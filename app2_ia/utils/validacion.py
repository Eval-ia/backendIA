import re
import logging
import pandas as pd

# Regex para detectar datos sensibles
DNI_RE = re.compile(r"\b\d{7,8}[A-Za-z]\b")
TEL_RE = re.compile(r"\b(\+34)?[ -]?[6-9]\d{8}\b")

# Columnas esperadas (todas en minúsculas)
COLUMNAS = {"candidato_id", "puesto", "fortalezas", "debilidades", "valoracion_gpt"}

logger = logging.getLogger(__name__)

def validar_filas(df: pd.DataFrame):
    """
    Valida cada fila de un DataFrame con columnas:
      candidato_id, puesto, fortalezas, debilidades, valoracion_gpt.

    - Verifica que las columnas concuerden.
    - Asegura que candidato_id sea numérico.
    - Fallback: si valoracion_gpt está vacío o NaN, lo construye
      concatenando fortalezas y debilidades.
    - Descarta filas con campos requeridos vacíos (excepto valoracion_gpt),
      o con datos sensibles (DNI/TEL).

    Returns:
        validos: List[dict] de filas corregidas (con valoracion_gpt siempre presente).
        errores: List[str] con mensajes de error por fila.
    """
    errores = []
    validos = []

    # Chequeo de columnas
    if set(df.columns.str.lower()) != COLUMNAS:
        raise ValueError(f"Columnas incorrectas. Se esperaba {COLUMNAS}, vino {set(df.columns)}")

    for i, row in df.iterrows():
        fila = row.to_dict()

        # 1) Campos requeridos no nulos (excepto valoracion_gpt)
        requeridos = ["candidato_id", "puesto", "fortalezas", "debilidades"]
        if any(pd.isnull(fila.get(c)) for c in requeridos):
            errores.append(f"Fila {i+2}: campos {requeridos} no pueden estar vacíos")
            continue

        # 2) Fallback de valoracion_gpt si viene vacío o NaN
        valoracion = fila.get("valoracion_gpt")
        if pd.isna(valoracion) or (isinstance(valoracion, str) and not valoracion.strip()):
            fortalezas = fila["fortalezas"].strip() or ""
            debilidades = fila["debilidades"].strip() or ""
            reconstruido = f"{fortalezas} {debilidades}".strip()
            fila["valoracion_gpt"] = reconstruido
            logger.debug(
                "Fila %d: valoracion_gpt ausente; usando '%s'", 
                i+2, reconstruido
            )

        # 3) ID numérico
        if not str(fila["candidato_id"]).isdigit():
            errores.append(f"Fila {i+2}: ID no numérico ('{fila['candidato_id']}')")
            continue

        # 4) Detección de datos sensibles
        texto_compuesto = " ".join(str(v) for v in fila.values())
        if DNI_RE.search(texto_compuesto) or TEL_RE.search(texto_compuesto):
            errores.append(f"Fila {i+2}: dato sensible detectado")
            continue

        # Si pasó todas las validaciones, la añadimos
        validos.append(fila)

    return validos, errores
