import os
import sys
import subprocess
import importlib.util
import venv
import logging
from pathlib import Path

# Verificar si estamos siendo importados por uvicorn
running_as_uvicorn_module = 'uvicorn' in sys.modules

# Verificar entorno virtual antes de importar otras dependencias
def is_venv():
    """Verifica si se está ejecutando en un entorno virtual"""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

# Si se está ejecutando como python -m uvicorn y no estamos en un entorno virtual
if running_as_uvicorn_module and not is_venv() and not os.environ.get('EVALIA_VENV_CHECKED'):
    # Marcar la verificación para evitar recursión
    os.environ['EVALIA_VENV_CHECKED'] = '1'
    
    # No estamos en un entorno virtual, debemos crear/usar uno
    print("\n" + "="*50)
    print("No se está ejecutando en un entorno virtual. Configurando...")
    print("="*50 + "\n")
    
    venv_dir = Path(__file__).resolve().parent.parent / ".venv"
    
    # Crear entorno virtual si no existe
    if not venv_dir.exists():
        print(f"Creando entorno virtual en {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    
    # Construir rutas para Windows
    python_exe = venv_dir / "Scripts" / "python.exe"
    pip_exe = venv_dir / "Scripts" / "pip.exe"
    
    # Verificar que el ejecutable de Python existe
    if not python_exe.exists():
        print(f"Error: No se encontró Python en el entorno virtual")
        sys.exit(1)
    
    # Instalar directamente desde requirements.txt usando pip_exe (el pip del entorno virtual)
    requirements_file = Path(__file__).resolve().parent.parent / "requirements.txt"
    
    if requirements_file.exists():
        print(f"Instalando dependencias desde {requirements_file}...")
        try:
            subprocess.check_call([
                str(pip_exe), "install", "-r", str(requirements_file)
            ])
            print("Dependencias instaladas correctamente")
        except Exception as e:
            print(f"Error instalando desde requirements.txt: {e}")
            print("Intentando instalar paquetes críticos individualmente...")
            
            # Si falla, instalar los paquetes críticos uno por uno usando pip_exe
            critical_packages = [
                "fastapi",
                "uvicorn",
                "pandas",
                "sqlalchemy",
                "pgvector",
                "python-multipart",
                "psycopg2-binary", 
                "spacy",
                "sentence-transformers"
            ]
            
            success = True
            for package in critical_packages:
                try:
                    print(f"Instalando {package}...")
                    subprocess.check_call([
                        str(pip_exe), "install", package
                    ])
                except Exception as pkg_e:
                    print(f"Error instalando {package}: {pkg_e}")
                    success = False
            
            if not success:
                print("Advertencia: Algunas dependencias no pudieron instalarse. Continuando de todos modos.")
    
    # Instalar modelo de spaCy usando python_exe (el python del entorno virtual)
    try:
        print("Instalando modelo de spaCy...")
        subprocess.check_call([
            str(python_exe), "-m", "spacy", "download", "es_core_news_sm"
        ])
    except Exception as e:
        print(f"Error instalando modelo de spaCy: {e}")
        # Continuamos de todos modos
    
    # En Windows, usar subprocess.Popen en lugar de os.execv
    print("Reiniciando aplicación en entorno virtual...")
    
    # Construir un comando específico y conocido
    cmd = [
        str(python_exe),
        "-m",
        "uvicorn",
        "app2_ia.main:app"
    ]
    
    # Añadir opciones como --reload si están presentes
    for arg in sys.argv:
        if arg.startswith("--"):
            cmd.append(arg)
    
    print(f"Comando: {' '.join(cmd)}")
    
    # Usar subprocess.Popen y sys.exit para detener este proceso
    process = subprocess.Popen(cmd)
    sys.exit(0)  # Salir de este proceso para dejar que el nuevo proceso tome el control

# Ahora importamos las dependencias de FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app2_ia.routes import ingest_controller, search_controller

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("app2_ia")

def setup_environment():
    """
    Verifica y configura el entorno de la aplicación.
    - Comprueba dependencias críticas
    - Instala solo las que faltan
    - Configura el modelo de spaCy
    
    Returns:
        bool: True si la configuración fue exitosa
    """
    # Verificar si spaCy está instalado correctamente
    try:
        import spacy
        logger.info("spaCy ya está instalado")
    except ImportError:
        logger.warning("spaCy no está instalado. Instalando...")
        try:
            # Usar el pip del entorno virtual actual (donde ya estamos ejecutando)
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "spacy"
            ])
            logger.info("spaCy instalado correctamente")
        except Exception as e:
            logger.error(f"Error instalando spaCy: {e}")
            return False
    
    # Verificar el modelo de spaCy
    try:
        import spacy
        try:
            nlp = spacy.load("es_core_news_sm")
            logger.info("Modelo de spaCy ya instalado")
        except OSError:
            logger.info("Instalando modelo de spaCy...")
            try:
                # Usar python del entorno virtual actual
                subprocess.check_call([
                    sys.executable, "-m", "spacy", "download", "es_core_news_sm"
                ])
                logger.info("Modelo de spaCy instalado correctamente")
            except Exception as e:
                logger.error(f"Error instalando modelo de spaCy: {e}")
                return False
    except Exception as e:
        logger.error(f"Error al verificar el modelo de spaCy: {e}")
        return False
    
    # Verificar otras dependencias críticas
    critical_packages = ["fastapi", "sqlalchemy", "sentence_transformers", "pgvector", "pandas"]
    missing_packages = []
    
    for pkg in critical_packages:
        if importlib.util.find_spec(pkg) is None:
            missing_packages.append(pkg)
    
    if missing_packages:
        logger.info(f"Instalando dependencias faltantes: {', '.join(missing_packages)}")
        try:
            for package in missing_packages:
                # Usar el pip del entorno virtual actual
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
            logger.info("Dependencias instaladas correctamente")
        except Exception as e:
            logger.error(f"Error instalando dependencias: {e}")
            return False
    
    return True

# Ejecutado solo cuando se inicia directamente (no al importar)
if __name__ == "__main__":
    # 1. Verificar entorno virtual
    if not is_venv():
        logger.warning("No se está ejecutando en un entorno virtual. Configurando...")
        venv_dir = Path(__file__).resolve().parent.parent / ".venv"
        
        # Crear entorno virtual si no existe
        if not venv_dir.exists():
            try:
                logger.info(f"Creando entorno virtual en {venv_dir}...")
                venv.create(venv_dir, with_pip=True)
            except Exception as e:
                logger.error(f"Error creando entorno virtual: {e}")
                sys.exit(1)
        
        # Preparar comando para reiniciar en el entorno virtual
        if os.name == "nt":  # Windows
            python_exe = venv_dir / "Scripts" / "python.exe"
        else:  # Unix/Linux
            python_exe = venv_dir / "bin" / "python"
        
        # Obtener argumentos originales
        script_path = os.path.abspath(sys.argv[0])
        cmd = [str(python_exe), script_path] + sys.argv[1:]
        
        logger.info(f"Reiniciando aplicación en entorno virtual...")
        os.execv(str(python_exe), cmd)
    
    # 2. Configurar entorno (ya estamos en entorno virtual)
    if not setup_environment():
        logger.error("Error configurando el entorno. Abortando.")
        sys.exit(1)
    
    logger.info("Entorno configurado correctamente. Iniciando aplicación...")

app = FastAPI(
    title="Eval-IA Backend",
    description="API para evaluación de candidatos mediante IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limitar a orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_controller.router, prefix="/api", tags=["Ingestión"])
app.include_router(search_controller.router, prefix="/api", tags=["Búsqueda"])

# Evento de inicio para confirmar estado del entorno
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    logger.info("Servicio API de Eval-IA iniciado correctamente")
    
    # Mostrar información de entorno
    if is_venv():
        venv_path = sys.prefix
        print(f"USANDO ENTORNO VIRTUAL: {venv_path}")
        logger.info(f"Ejecutando en entorno virtual: {venv_path}")
    else:
        print("NO SE ESTÁ USANDO UN ENTORNO VIRTUAL")
        logger.warning("No se está ejecutando en un entorno virtual. Esto no es recomendable.")
        
    # Verificar dependencias si aún no se han verificado
    if not os.environ.get('EVALIA_DEPS_CHECKED'):
        os.environ['EVALIA_DEPS_CHECKED'] = '1'
        if not setup_environment():
            logger.warning("Problemas configurando el entorno, pero intentando continuar...")