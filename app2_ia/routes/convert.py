from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/convertir_csv_a_json")
async def convertir_csv_a_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    try:
        df = pd.read_csv(file.file)
        json_data = df.to_dict(orient="records")  # Convertimos a lista de diccionarios
        return {"datos": json_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")

