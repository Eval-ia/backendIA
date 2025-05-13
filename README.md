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
