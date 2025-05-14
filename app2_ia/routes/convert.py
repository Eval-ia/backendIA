from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import re
from datetime import datetime

router = APIRouter()

# Columnas requeridas
COLUMNAS_ESPERADAS = [
    "candidato_id",
    "puesto",
    "fortalezas",
    "debilidades",
    "valoracion_gpt"
]

# Patrones para datos sensibles
PATRON_DNI = re.compile(r"\b\d{7,8}[A-Za-z]\b|\b\d{8}-?[A-Za-z]\b")
PATRON_TELEFONO = re.compile(r"\b(\+34)?[ -]?[6-9]\d{8}\b")

@router.post("/convertir_csv_a_json")
async def convertir_csv_a_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    try:
        df = pd.read_csv(file.file)

        # 1. Verificar estructura de columnas
        if set(df.columns.str.lower()) != set(COLUMNAS_ESPERADAS):
            raise HTTPException(status_code=400, detail="El CSV no tiene las columnas requeridas exactas.")

        filas_validas = []
        errores = []

        for idx, row in df.iterrows():
            fila_num = idx + 2  # para indicar número de línea (incluyendo cabecera)
            error = None

            # 2. Verificar campos vacíos
            if row.isnull().any():
                error = "Campos vacíos"

            # 3. Verificar ID numérico
            elif not str(row["candidato_id"]).strip().isdigit():
                error = "ID no numérico"

            # 4. Verificar datos sensibles
            else:
                for col in df.columns:
                    value = str(row[col])
                    if PATRON_DNI.search(value) or PATRON_TELEFONO.search(value):
                        error = f"Dato sensible en '{col}'"
                        break

            # 5. Clasificar la fila
            if error:
                errores.append(f"Fila {fila_num}: {error} → {row.to_dict()}")
            else:
                filas_validas.append(row.to_dict())

        # 6. Guardar errores en log si hay
        if errores:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"errores_{timestamp}.log"
            with open(log_file, "w", encoding="utf-8") as f:
                for err in errores:
                    f.write(err + "\n")
            print(f"[INFO] Log guardado: {log_file}")

        return {
            "validados": len(filas_validas),
            "descartados": len(errores),
            "datos": filas_validas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")
