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
     # Paso 1: validar el CSV
    candidatos_validos, errores = cargar_y_validar_csv(file)

    # Paso 2: procesar sólo los válidos
    try:
        resultado: ResultadoCarga = procesar_y_guardar_candidatos(candidatos_validos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

    # Paso 3: completar el resultado con los errores y descartados
    resultado.descartados = len(errores)
    resultado.errores = errores

    return resultado