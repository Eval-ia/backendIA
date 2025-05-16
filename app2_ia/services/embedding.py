# service/embedding.py
"""
Módulo 3: Sistema de Embeddings con 1536 dimensiones
Aplicación App2 - Evaluación de Candidatos mediante IA

Este módulo genera embeddings de 1536 dimensiones usando Sentence-Transformers
con una capa de proyección adicional para alcanzar las dimensiones deseadas.
"""

import logging
from typing import List
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuración de logging
logger = logging.getLogger(__name__)


class EmbeddingModule:
    """
    Módulo 3: Generador de Embeddings de 1536 dimensiones
    
    Usa Sentence-Transformers con proyección lineal para generar
    embeddings de exactamente 1536 dimensiones.
    """
    
    def __init__(self):
        """
        Inicializa el módulo de embeddings
        """
        self.target_dim = 1536  # Dimensiones objetivo
        self._cache = {}  # Cache manual para embeddings
        self._initialize_model()
        logger.info(f"Módulo 3 inicializado - Embeddings de {self.target_dim} dimensiones")
    
    def _initialize_model(self):
        """Inicializa el modelo y la matriz de proyección"""
        # Usar un modelo de 768 dimensiones como base
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.base_dim = 768  # Dimensiones del modelo base
        
        # Crear matriz de proyección para expandir a 1536 dimensiones
        # Usar una inicialización determinista
        np.random.seed(42)
        self.projection_matrix = np.random.randn(self.base_dim, self.target_dim)
        # Normalizar la matriz para evitar explosión de gradientes
        self.projection_matrix = self.projection_matrix / np.sqrt(self.base_dim)
        
        logger.info(f"Modelo base cargado ({self.base_dim}D) con proyección a {self.target_dim}D")
    
    def _project_to_target_dim(self, embedding: np.ndarray) -> List[float]:
        """
        Proyecta el embedding a las dimensiones objetivo (1536)
        
        Args:
            embedding: Embedding original del modelo base
            
        Returns:
            Embedding proyectado a 1536 dimensiones
        """
        # Proyectar usando multiplicación matricial
        projected = np.dot(embedding, self.projection_matrix)
        
        # Normalizar para mantener la magnitud
        norm = np.linalg.norm(projected)
        if norm > 0:
            projected = projected / norm
        
        return projected.tolist()
    
    def _generate_cache_key(self, texto: str) -> str:
        """Genera una clave única para el cache basada en el texto"""
        return hashlib.md5(texto.encode()).hexdigest()
    
    def _cached_embedding(self, cache_key: str, texto: str) -> List[float]:
        """
        Genera embedding con cache para evitar recálculos
        
        Args:
            cache_key: Clave única para el cache
            texto: Texto a procesar
            
        Returns:
            Lista de floats representando el embedding de 1536 dimensiones
        """
        # Verificar si está en cache
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Generar embedding base
        embedding_base = self.model.encode(texto)
        
        # Proyectar a 1536 dimensiones
        embedding_1536 = self._project_to_target_dim(embedding_base)
        
        # Guardar en cache
        self._cache[cache_key] = embedding_1536
        
        # Limitar tamaño del cache
        if len(self._cache) > 1000:
            # Eliminar el primer elemento (FIFO)
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        
        return embedding_1536
    
    def generar_embedding(self, texto_limpio: str) -> List[float]:
        """
        Genera embedding para un texto limpio
        
        Args:
            texto_limpio: Texto preprocesado a convertir en embedding
            
        Returns:
            Lista de floats de 1536 dimensiones
        """
        # Manejo de texto vacío
        if not texto_limpio.strip():
            texto_limpio = " "
        
        # Generar clave de cache
        cache_key = self._generate_cache_key(texto_limpio)
        
        # Generar embedding (con cache)
        embedding = self._cached_embedding(cache_key, texto_limpio)
        
        # Retornar directamente la lista
        return embedding


# Instancia global del módulo (singleton pattern)
_modulo_singleton = None

def obtener_modulo() -> EmbeddingModule:
    """
    Obtiene la instancia singleton del módulo
    
    Returns:
        Instancia del módulo de embeddings
    """
    global _modulo_singleton
    if _modulo_singleton is None:
        _modulo_singleton = EmbeddingModule()
    return _modulo_singleton


# Función principal para integración con pipeline
def generar_embedding(texto_limpio: str) -> List[float]:
    """
    Función de interfaz para el pipeline
    
    Args:
        texto_limpio: Texto preprocesado a convertir en embedding
        
    Returns:
        Lista de floats de 1536 dimensiones
    """
    # Obtener instancia del módulo
    modulo = obtener_modulo()
    
    # Generar embedding
    return modulo.generar_embedding(texto_limpio)