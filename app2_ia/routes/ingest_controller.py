from fastapi import APIRouter, UploadFile, File, HTTPException
from app2_ia.services import cargar_y_validar_csv
from app2_ia.models.schemas import procesar_y_guardar_candidatos

router = APIRouter()

@router.post("/procesar_csv_completo")
async def procesar_csv_completo(file: UploadFile = File(...)):
    try:
        # Paso 1: validar el CSV y convertirlo a JSON
        candidatos_validos, errores = cargar_y_validar_csv(file)

        # Paso 2: procesar y guardar en VectorDB
        procesar_y_guardar_candidatos(candidatos_validos)

        return {"mensaje": "Proceso completado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
