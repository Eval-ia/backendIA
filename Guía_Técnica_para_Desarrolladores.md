# Eval-IA – Guía Técnica para Desarrolladores

Este documento está pensado como guía de traspaso para quien continúe el desarrollo o mantenimiento del proyecto **Eval-IA – Backend de Evaluación de Candidatos mediante IA**.

---

## Descripción General

App2 es un microservicio de backend escrito en **Python 3.11+ con FastAPI**, que:

- Recibe informes de candidatos desde App1 (formato CSV)
- Limpia, transforma y vectoriza el texto evaluativo (valoración GPT)
- Guarda los embeddings y metadatos en una **base de datos vectorial (PostgreSQL + pgvector)**
- Expone endpoints para **consultar candidatos similares a un perfil ideal**

---

## Arquitectura Modular

```text
 App1 (generador de informes CSV)
           ⬇
     /api/procesar_csv_completo     ---> Módulo de Ingesta
           ⬇
   [Preprocesamiento (SpaCy)]       ---> Módulo 2
           ⬇
   [Embeddings (SentenceTransformers + Proyección)] ---> Módulo 3
           ⬇
   [VectorDB (PostgreSQL + pgvector)] ---> Módulo 4
           ⬇
   /api/buscar_similares            ---> Módulo 5
```

---

## Estructura Principal del Proyecto

```
app2_ia/
├── models/schemas.py
├── services/
│   ├── ingest_service.py
│   ├── embedding.py
│   ├── vector_db.py
│   ├── search_service.py
│   ├── clustering_service.py
│   ├── reranking_service.py
├── utils/
│   ├── limpieza.py
│   ├── validacion.py
├──  scripts/
│     └── train_reranking.py
├── routes/
│   ├── ingest_controller.py
│   ├── search_controller.py
├── data/
│   └── reranking_train.json  
├── models/
│   └── reranker.joblib  
│
├── requirements3.txt
└── main.py
```

---

## Flujo de Procesamiento

### 1. Ingesta de CSV (`/api/procesar_csv_completo`)
- Valida el archivo CSV
- Limpia el texto de `valoracion_gpt`
- Genera embedding (1536D)
- Inserta en la base de datos vectorial

### 2. Búsqueda Semántica (`/api/buscar_similares`)
- Limpia el texto de entrada
- Genera embedding de referencia
- Busca candidatos más similares (cosine_distance)
- Aplica clustering KMeans para agrupar los candidatos por similitud semántica
- Aplica reranking supervisado con XGBoost utilizando [similitud, cluster_id] como features
- Reordena los candidatos por adjusted_score y actualiza su posición en el ranking
- Devuelve `ResultadoRanking` con top 10

---

## Base de Datos Vectorial

**PostgreSQL + pgvector**

Tabla: `evalia_embeddings`

Campos:

- `candidato_id` (int)
- `puesto` (str)
- `embedding` (Vector[1536])
- `fortalezas` (str)
- `debilidades` (str)
- `fecha_de_creacion` (date)


---

## Consideraciones Importantes

- Se descartan:
  - IDs no numéricos
  - Campos vacíos
  - Datos sensibles (DNI, teléfono)
- Logs en `logs/errores_TIMESTAMP.log`
- Cache de embeddings incluido
- Resultados retornan solo `candidato_id` y `similitud` (sin datos personales)

---

## Setup Rápido para Desarrollo

```bash
git clone https://github.com/Eval-ia/backendIA.git
cd backendIA
pip install uvicorn fastapi
python -m uvicorn app2_ia.main:app
```

Visita: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Checklist de Buenas Prácticas

- [ ] Validar bien los CSV
- [ ] Documentar los errores encontrados
- [ ] Cuidar rendimiento del embedding (cache)
- [ ] Revisar búsquedas por `puesto`
- [ ] Usar `.env` para las credenciales y configuración

---

## Tareas Futuras Sugeridas

- Agregar autenticación JWT
- Incluir visualización de resultados (frontend)
- Exportar resultados y errores como CSV
- Añadir tests automatizados (pytest)
- Añadir gráficas de candidaturas.
- Ampliar el dataset de entrenamiento con ejemplos reales o etiquetados por RRHH
- Incorporar nuevas features al modelo (longitud_texto, match_palabras_clave, etc.).
- Optimizar el número de clústeres dinámicamente según los candidatos (Silhouette, Elbow method).
- Evaluar el rendimiento del modelo con métricas de ranking como NDCG o MRR.