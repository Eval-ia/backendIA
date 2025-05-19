# Eval-IA – Backend de Inteligencia Artificial para Evaluación de Candidatos

Este proyecto es un microservicio de backend desarrollado en **Python + FastAPI**, que proporciona un sistema de evaluación inteligente de candidatos mediante procesamiento de lenguaje natural y vectorización semántica.

Forma parte del sistema Eval-IA, y se comunica con una app principal (App1) que genera informes de evaluación técnica.

---

## 🚀 Objetivos del Proyecto

- Recibir informes de entrevistas (texto libre o estructurado)
- Preprocesar y vectorizar los contenidos
- Almacenar representaciones vectoriales con metadatos
- Comparar candidatos con perfiles ideales
- Devolver rankings automáticos para apoyar decisiones de RRHH

---

## ⚙️ Stack Tecnológico

- **Python 3.11+**
- **FastAPI** (API REST)
- **Sentence Transformers** (embeddings semánticos)
- **FAISS** (almacenamiento y búsqueda vectorial)
- **Uvicorn** (servidor ASGI)

---

## 🧑‍💻 Instalación del entorno (Mac / Linux / Windows)


Sigue los siguientes pasos para configurar el entorno localmente y poder trabajar en el backend IA.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Eval-ia/backendIA.git
cd backendIA

2. Crear entorno virtual de Python
python3 -m venv venv

3. Activar entorno virtual
En Mac/Linux:
  source venv/bin/activate
En Windows:
  .\venv\Scripts\activate

4. Instalar las dependencias
pip install -r requirements.txt

5. Ejecutar la aplicación en modo desarrollo
uvicorn app2_ia.main:app --reload

6. Acceder a la documentación de la API
Una vez arrancado el servidor, visita:

http://localhost:8000/docs
(Interfaz Swagger generada automáticamente por FastAPI)

✅ Consejo: ejecuta deactivate cuando termines para cerrar el entorno virtual.



Flujo de Datos entre App1 y App2 (versión final)

📁 Formato de CSV enviado desde App1 a App2

CSV obligatorio con los siguientes campos:

candidato_id,puesto,fortalezas,debilidades,valoracion_gpt
1,Marketing,Creatividad y comunicación,Organización,"El candidato demuestra iniciativa y claridad, pero debe mejorar su planificación."
2,Marketing,Estrategia digital,Gestión del tiempo,"Tiene buena visión estratégica, pero dificultad en cumplir plazos."

🔹 valoracion_gpt es un campo obligatorio que contiene el texto generado por GPT (resumen evaluativo). 🔹 fortalezas y debilidades también deben estar presentes y reflejar lo indicado por GPT.

📄 JSON generado por el Módulo 1 (API FastAPI)

[
  {
    "candidato_id": "1",
    "puesto": "Marketing",
    "fortalezas": "Creatividad y comunicación",
    "debilidades": "Organización",
    "texto": "El candidato demuestra iniciativa y claridad, pero debe mejorar su planificación."
  },
  {
    "candidato_id": "2",
    "puesto": "Marketing",
    "fortalezas": "Estrategia digital",
    "debilidades": "Gestión del tiempo",
    "texto": "Tiene buena visión estratégica, pero dificultad en cumplir plazos."
  }
]

💡 Flujo modular en App2

Módulo 2 (Preprocesamiento)

📈 Entrada: { "texto": "..." }

🔄 Salida: { "texto_limpio": "..." }

Módulo 3 (Embeddings)

📈 Entrada: texto_limpio

🔄 Salida: embedding: List[float]

Módulo 4 (VectorDB)

📈 Entrada:

{
  "candidato_id": "1",
  "puesto": "Marketing",
  "embedding": [...],
  "metadata": {
    "fortalezas": "...",
    "debilidades": "..."
  }
}

Módulo 5 (Ranking)

📈 Entrada:

{
  "embedding_referencia": [...],
  "candidatos": [
    {"candidato_id": "1", "embedding": [...]},
    {"candidato_id": "2", "embedding": [...]}
  ]
}

🔄 Salida:

[
  {"candidato_id": "1", "similitud": 0.91, "ranking": 1},
  {"candidato_id": "2", "similitud": 0.86, "ranking": 2}
]

🗋 Contratos de datos (Pydantic)

class InformeEvaluacion(BaseModel):
    candidato_id: str
    puesto: str
    fortalezas: str
    debilidades: str
    texto: str

class TextoLimpio(BaseModel):
    texto_limpio: str

class EmbeddingCandidato(BaseModel):
    candidato_id: str
    puesto: str
    embedding: List[float]

class EntradaRanking(BaseModel):
    embedding_referencia: List[float]
    candidatos: List[EmbeddingCandidato]

class ResultadoRanking(BaseModel):
    candidato_id: str
    similitud: float
    ranking: int

🔎 Observaciones

La App2 no maneja nombres ni datos personales.

La App1 es responsable de mapear candidato_id a nombre u otros datos sensibles.

El campo texto es el input principal para IA.

El sistema está preparado para recibir y evaluar múltiples candidatos en un solo CSV.

El resultado siempre se devuelve en base a IDs y puntuación de similitud, sin juicio final automatizado.
