import re
import logging
import pandas as pd

# Configuración de logging
tools_logger = logging.getLogger(__name__)
tools_logger.setLevel(logging.INFO)

# Regex para detectar datos sensibles
DNI_RE = re.compile(r"\b\d{7,8}[A-Za-z]\b")
TEL_RE = re.compile(r"\b(\+34)?[ -]?[6-9]\d{8}\b")

# Columnas esperadas (todas en minúsculas)
COLUMNAS = {"candidato_id", "puesto", "fortalezas", "debilidades", "valoracion_gpt"}


def validar_filas(df: pd.DataFrame):
    """
    Valida cada fila de un DataFrame:
      - Normaliza cabeceras a minúsculas.
      - Verifica columnas esperadas.
      - Comprueba campos requeridos no vacíos.
      - Valida que candidato_id sea numérico (como texto).
      - Realiza fallback de valoracion_gpt si está vacío.
      - Descarta filas con datos sensibles (DNI/TEL).

    Retorna:
        validos: List[dict]
        errores: List[str]
    """
    errores = []
    validos = []

    # Normalizar nombres de columna
    df.columns = df.columns.str.lower()
    if set(df.columns) != COLUMNAS:
        raise ValueError(f"Columnas incorrectas. Se esperaba {COLUMNAS}, vino {set(df.columns)}")

    for i, row in df.iterrows():
        linea = i + 2
        fila = row.to_dict()

        # 1) Campos requeridos
        requeridos = ["candidato_id", "puesto", "fortalezas", "debilidades"]
        if any(pd.isna(fila[c]) or (isinstance(fila[c], str) and not fila[c].strip())
               for c in requeridos):
            msg = f"Fila {linea}: campos {requeridos} no pueden estar vacíos"
            tools_logger.warning(msg)
            errores.append(msg)
            continue

        # 2) ID numérico
        cid = str(fila["candidato_id"]).strip()
        if not cid.isdigit():
            msg = f"Fila {linea}: ID no numérico ('{fila['candidato_id']}')"
            tools_logger.warning(msg)
            errores.append(msg)
            continue
        fila["candidato_id"] = cid

        # 3) Fallback valoracion_gpt
        val = fila.get("valoracion_gpt")
        if pd.isna(val) or (isinstance(val, str) and not val.strip()):
            fort = fila["fortalezas"].strip()
            deb = fila["debilidades"].strip()
            reconstruido = f"{fort} {deb}".strip()
            fila["valoracion_gpt"] = reconstruido
            tools_logger.debug("Fila %d: valoracion_gpt ausente; usando '%s'", linea, reconstruido)

        # 4) Detectar datos sensibles
        texto = " ".join(fila.values())
        if DNI_RE.search(texto) or TEL_RE.search(texto):
            msg = f"Fila {linea}: dato sensible detectado"
            tools_logger.warning(msg)
            errores.append(msg)
            continue

        validos.append(fila)

    return validos, errores