from fastapi import APIRouter, UploadFile, File, HTTPException
from app2_ia.services.ingest_service import cargar_y_validar_csv, procesar_y_guardar_candidatos
from app2_ia.models.schemas import ResultadoCarga

router = APIRouter()

@router.post(
    "/procesar_csv_completo",
    response_model=ResultadoCarga,
    summary="Valida CSV, procesa embeddings y guarda en la BD vectorial"
)
async def procesar_csv_completo(file: UploadFile = File(...)):
    # Paso 1: validar el CSV y convertirlo a JSON
    candidatos_validos, errores = cargar_y_validar_csv(file)

    # Si hubo errores en validación, devolvemos 400 con detalles
    if errores:
        raise HTTPException(
            status_code=400,
            detail={"mensaje": "Errores en validación de CSV", "errores": errores}
        )

    # Paso 2: procesar y guardar en VectorDB, obteniendo el resultado completo
    try:
        resultado: ResultadoCarga = procesar_y_guardar_candidatos(candidatos_validos)
        return resultado
    except Exception as e:
        # Aquí podríamos diferenciar tipos de fallo (I/O, embedding, BD) según la excepción
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
