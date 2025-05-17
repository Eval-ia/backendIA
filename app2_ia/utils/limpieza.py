import spacy
import logging

# --- Configuración de logging para guardar en un archivo ---
# Esto configura el logger raíz.
# - level=logging.INFO: Se capturarán mensajes de INFO, WARNING, ERROR, CRITICAL.
# - format: Define el formato de los mensajes de log.
# - datefmt: Define el formato de la fecha/hora.
# - filename: Nombre del archivo donde se guardarán los logs.
# - filemode='a': 'a' (append) para añadir logs al final del archivo si ya existe.
#                  Usa 'w' (write) para sobrescribir el archivo en cada ejecución.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='errores_formateotext.log',
    filemode='a'
)

# Obtener un logger específico para este módulo (buena práctica)
logger = logging.getLogger(__name__)

# --- Carga del modelo de spaCy ---
# Es buena práctica cargarlo una vez fuera de la función si la vas a llamar múltiples veces.
nlp = None # Inicializar nlp a None
try:
    # Intentamos cargar un modelo en español.
    # 'es_core_news_sm' es pequeño y rápido.
    # Para mayor precisión, considera 'es_core_news_md' o 'es_core_news_lg'
    # (necesitarás descargarlos primero: python -m spacy download es_core_news_md)
    nlp = spacy.load('es_core_news_sm')
    logger.info("Modelo de spaCy 'es_core_news_sm' cargado exitosamente.")
except OSError:
    logger.error(
        "Modelo 'es_core_news_sm' no encontrado. "
        "Por favor, descárgalo ejecutando: python -m spacy download es_core_news_sm. "
        "El procesamiento de texto no funcionará sin el modelo."
    )
    # nlp permanece como None, la función lo manejará

def limpiar_texto_para_embedding(texto: str) -> str:
    """
    Limpia y procesa un texto en español para su uso en modelos de embedding.
    Incluye: conversión a minúsculas, eliminación de puntuación,
    eliminación de stopwords y lematización. Utiliza logging para errores/warnings
    y guarda los logs en un archivo.

    Args:
        texto (str): El texto de entrada a procesar.

    Returns:
        str: El texto procesado como un string único con tokens limpios y lematizados.
             Devuelve un string vacío si el modelo de spaCy no está cargado o el texto es nulo/vacío.
    """
    if nlp is None:
        logger.warning(
            "Intento de procesar texto ('%s...') pero el modelo de spaCy no está cargado. "
            "La función devolverá un string vacío.", texto[:20] if texto else "N/A"
        )
        return "" # Retorna string vacío si el modelo no se pudo cargar

    if not texto: # Verifica si el texto es None o vacío
        logger.info("Se recibió un texto vacío o None para procesar. Devolviendo string vacío.")
        return ""

    # Convertir texto a minúsculas
    texto_minusculas = texto.lower()
    logger.debug(f"Texto convertido a minúsculas: '{texto_minusculas[:50]}...'")

    # Procesar el texto con spaCy
    doc = nlp(texto_minusculas)

    tokens_limpios_lematizados = []
    for token in doc:
        # Filtrar puntuación y stopwords
        # token.is_alpha puede ser útil si solo quieres palabras (sin números o símbolos especiales)
        if not token.is_punct and not token.is_stop:
            tokens_limpios_lematizados.append(token.lemma_)
            logger.debug(f"Token: '{token.text}' -> Lemma: '{token.lemma_}', No es Puntuación, No es Stopword")
        else:
            logger.debug(f"Token: '{token.text}' -> Descartado (Puntuación: {token.is_punct}, Stopword: {token.is_stop})")


    resultado = " ".join(tokens_limpios_lematizados)
    logger.info(f"Texto original ('{texto[:30]}...') procesado a ('{resultado[:30]}...').")
    return resultado
