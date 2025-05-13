## 🔧 Instalación del entorno (Mac / Linux / Windows)

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

