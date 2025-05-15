import re
import pandas as pd

DNI_RE = re.compile(r"\b\d{7,8}[A-Za-z]\b")
TEL_RE = re.compile(r"\b(\+34)?[ -]?[6-9]\d{8}\b")

COLUMNAS = {"candidato_id", "puesto", "fortalezas", "debilidades", "valoracion_gpt"}

def validar_filas(df):
    errores = []
    validos = []

    if set(df.columns.str.lower()) != COLUMNAS:
        raise ValueError("Columnas incorrectas")

    for i, row in df.iterrows():
        fila = row.to_dict()
        if any(pd.isnull(v) for v in fila.values()):
            errores.append(f"Fila {i+2}: campos vacíos")
            continue
        if not str(fila["candidato_id"]).isdigit():
            errores.append(f"Fila {i+2}: ID no numérico")
            continue
        if any(DNI_RE.search(str(v)) or TEL_RE.search(str(v)) for v in fila.values()):
            errores.append(f"Fila {i+2}: dato sensible")
            continue
        validos.append(fila)

    return validos, errores
