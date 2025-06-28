# services/vector_db.py

# ----------------------
# Importación de librerías y configuración
# ----------------------
import os  # Leer variables de entorno
from datetime import date  # Fecha por defecto
from sqlalchemy import create_engine, Column, Integer, String, Date  # Core SQLAlchemy
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base, sessionmaker  # ORM base y sesiones
from pgvector.sqlalchemy import Vector  # Tipo vectorial de pgvector
from typing import Dict, Any, List  # Anotaciones de tipos


# --------------------------------------------------
# Configuración de la conexión a la base de datos
# --------------------------------------------------
# Leemos la URL de conexión desde la variable de entorno DATABASE_URL.
# Si no está definida, se conecta por defecto al servidor remoto especificado.
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Tienes que definir la variable de entorno DATABASE_URL")

# -----------------------
# Definición del modelo ORM
# -----------------------
# Clase base para todos los modelos
Base = declarative_base()

class EmbeddingCandidato(Base):
    """
    Modelo que representa la tabla 'evalia_embeddings' en PostgreSQL.
    Cada fila almacena un embedding de candidato y su metadata.
    """
    __tablename__ = 'evalia_embeddings'

    # Clave primaria auto-incremental
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Identificador numérico del candidato
    candidato_id = Column(Integer, nullable=False)
    # Nombre o código del puesto al que aplica
    puesto = Column(String, nullable=False)
    # Columna vectorial para almacenar embeddings de 1536 dimensiones
    embedding = Column(Vector(1536),nullable=False)
    # Metadatos: fortalezas extraídas del informe
    fortalezas = Column(Text, nullable=True)
    # Metadatos: debilidades extraídas del informe
    debilidades = Column(Text, nullable=True)
    # Fecha de creación del registro (valor por defecto: fecha actual)
    fecha_de_creacion = Column(Date, default=date.today, nullable=False)

# ---------------------------
# Inicialización de SQLAlchemy
# ---------------------------
# Crea el engine para conectar con la base de datos usando DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    connect_args={
      "sslmode": "disable",
      # Esto ejecuta al conectar: SET client_encoding TO 'latin1'
      "options": "-c client_encoding=latin1"
    }
)
# Factoría de sesiones; cada sesión representa una transacción
SessionLocal = sessionmaker(bind=engine)
# Crea las tablas definidas en los modelos si no existen en la base de datos
Base.metadata.create_all(bind=engine)

# --------------------------------------
# Función para insertar un embedding
# --------------------------------------

def insertar_en_vectordb(objeto_final: Dict[str, Any]) -> None:
    """
    Inserta un embedding de candidato y sus metadatos en la tabla 'evalia_embeddings'.

    Parámetros:
      objeto_final (dict) con claves:
        - 'candidato_id': int o str convertible a int
        - 'puesto': str
        - 'embedding': List[float] (vector de 1536 floats)
        - 'metadata': dict con keys 'fortalezas', 'debilidades', 'fuente'
    """
    # Abrimos una nueva sesión para la transacción
    session = SessionLocal()
    try:
        # Construimos el objeto ORM con los datos proporcionados
        record = EmbeddingCandidato(
            candidato_id=int(objeto_final['candidato_id']),
            puesto=objeto_final['puesto'],
            embedding=objeto_final['embedding'],
            fortalezas=objeto_final['metadata'].get('fortalezas'),
            debilidades=objeto_final['metadata'].get('debilidades'),
        )
        # Añadimos el registro a la sesión
        session.add(record)
        # Ejecutamos el INSERT en la base de datos
        session.commit()
    except Exception as e:
        # Si hay error, revertimos cambios y propagamos la excepción
        session.rollback()
        raise RuntimeError(f"Error al insertar en la base de datos vectorial: {e}")
    finally:
        # Cerramos la sesión para liberar recursos
        session.close()

def existe_candidato(candidato_id: int) -> bool:
    """
    Verifica si ya existe un candidato con ese ID en la tabla 'evalia_embeddings'.
    """
    session = SessionLocal()
    try:
        existe = session.query(EmbeddingCandidato).filter_by(candidato_id=candidato_id).first()
        return existe is not None
    except Exception as e:
        raise RuntimeError(f"Error al comprobar existencia en VectorDB: {e}")
    finally:
        session.close()
 
