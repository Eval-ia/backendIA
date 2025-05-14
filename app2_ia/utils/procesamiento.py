import json
import re
import string
import spacy

# Cargar el modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Descargando modelo de spaCy para español ('es_core_news_sm')...")
    print("Ejecuta 'python -m spacy download es_core_news_sm' en tu terminal si falla.")
    raise


def preparar_datos_para_limpiar(lista_de_registros):
    """
    Adapta una lista de registros (con 'valoracion_gpt') al formato esperado
    para la limpieza (lista de diccionarios con 'texto').

    Args:
        lista_de_registros (list): Lista donde cada elemento es un dict
                                   con la clave 'valoracion_gpt'.

    Returns:
        list: Lista de diccionarios con la clave 'texto'.
    """
    # Asegurarse de que la entrada es una lista
    if not isinstance(lista_de_registros, list):
         print(f"Error: Se esperaba una lista de registros, pero se recibió {type(lista_de_registros)}.")
         return [] # O manejar el error de otra forma

    # Usar una comprensión de lista para transformar los datos
    # Incluimos un manejo básico si un registro no es un dict o no tiene la clave
    datos_formato_limpieza = []
    for registro in lista_de_registros:
        if isinstance(registro, dict) and "valoracion_gpt" in registro and registro["valoracion_gpt"] is not None:
             # Asegurarse de que el valor es un string antes de intentar acceder
             if isinstance(registro["valoracion_gpt"], str):
                 datos_formato_limpieza.append({"texto": registro["valoracion_gpt"]})
             else:
                 print(f"Advertencia: El valor para 'valoracion_gpt' no es un string en un registro. Valor: {registro['valoracion_gpt']}. Saltando o tratando como vacío.")
                 datos_formato_limpieza.append({"texto": ""}) # Añadir vacío si no es string
        else:
             print(f"Advertencia: Registro no tiene el formato esperado (dict con clave 'valoracion_gpt' no nula). Registro: {registro}. Saltando.")
             # Opcional: añadir un registro vacío si necesitas mantener la correspondencia
             # datos_formato_limpieza.append({"texto": ""})


    return datos_formato_limpieza


# --- Función de limpieza y normalización ---
def limpiar_y_normalizar_texto(texto):
    """
    Limpia y normaliza un string de texto para prepararlo para embedding.
    (Código de esta función es el mismo que antes, usa spaCy)
    """
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = re.sub(r'\d+', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    doc = nlp(texto)
    palabras_procesadas = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space and token.text.strip() != ''
    ]

    texto_normalizado = ' '.join(palabras_procesadas)
    return texto_normalizado


def procesar_lista_formato_limpieza(datos_formato_limpieza):
    """
    Procesa una lista de diccionarios con clave 'texto', limpiando cada texto.

    Args:
        datos_formato_limpieza (list): Lista de diccionarios con la clave 'texto',
                                       resultado de preparar_datos_para_limpiar.

    Returns:
        list: Una lista de strings, donde cada string es el texto normalizado.
    """
    informes_normalizados = []

    if not isinstance(datos_formato_limpieza, list):
        print(f"Error: La entrada a procesar_lista_formato_limpieza no es una lista. Tipo: {type(datos_formato_limpieza)}")
        return []

    # Iterar sobre cada objeto (informe ya preparado) en la lista
    for i, informe_obj in enumerate(datos_formato_limpieza):
        # Asegurarse de que el objeto es un diccionario y contiene la clave 'texto'
        if isinstance(informe_obj, dict) and "texto" in informe_obj:
            texto_original = informe_obj["texto"]
            # Limpiar y normalizar el texto usando la función auxiliar
            texto_limpio = limpiar_y_normalizar_texto(texto_original)
            informes_normalizados.append(texto_limpio)
        else:
            # Este error debería ser menos común si preparar_datos_para_limpiar funciona bien
            print(f"Advertencia: Elemento en la posición {i} no tiene el formato esperado (dict con clave 'texto'). Saltando.")


    return informes_normalizados
