## **Línea Temporal del Proyecto Eval-IA (13 al 22 de mayo de 2025)**

### 🟩 **Inicio y Preparación del Proyecto**

📅 **13 mayo 2025**

- Estructura inicial del repositorio creada (`Initial clean commit`, `README`, carpetas `app2_ia/`)
- Se realizaron múltiples merges de ramas vacías/iniciales.
- ✅ *Inicio del repositorio, estructura base, definición de módulos.*

**⏱ Duración estimada:** 1 día

---

### 🟦 **Módulo 1: Ingesta y Validación de CSV**

📅 **13–14 mayo 2025**

- Implementación del procesamiento CSV, validaciones básicas, detección de datos sensibles, logs (`defe4e1`, `56ac2d1`, `ea44e12`)
- Múltiples merges relacionados con `modulo_01` y `modulo2/utils`.

**⏱ Duración estimada:** 1.5 días

---

### 🟨 **Módulo 2–3: Limpieza de texto y generación de embeddings**

📅 **14–15 mayo 2025**

- Limpieza de texto con spaCy (`Función nueva`, `Quitamos schema no usado`)
- Embedding funcional y proyección (`Creación de embedding funcional`, `Mejoras Globales`, `Inserción en BD funcionando`)

**⏱ Duración estimada:** 2 días

---

### 🟧 **Módulo 4: Almacenamiento en vector DB con pgvector**

📅 **15 mayo 2025**

- Función de inserción en vector DB (`Insercción a la base de datos funciona correctamente`)
- Revisión de `requirements`, estructura final estable

**⏱ Duración estimada:** 1 día

---

### 🟥 **Módulo 5: Búsqueda vectorial y ranking por similitud**

📅 **14–20 mayo 2025**

- Desarrollo del endpoint `/buscar_similares` (`Controller y service búsqueda`, `calculo de similitud`)
- Control de duplicados, validaciones adicionales
- Refactorizaciones finales y mejoras (`version con límite en query`, `corrección duplicidad datos`)

**⏱ Duración estimada:** 4–5 días

---

### 🟪 **Fase Final y Estabilización**

📅 **20–21 mayo 2025**

- Implementación de validaciones finales, límite en consultas, y pruebas de endpoints
- Commits destacados: `Merge pull request #17`, `version_limite`, `línea_de_trabajo.md`

**⏱ Duración estimada:** 1.5 días

---

### 🟫 **Módulo Extra: Clustering y Machine Learning**

📅 **21–22 mayo 2025**

- Implementación de un modelo de clustering (`clustering`, `Implementación modelo ML`)
- Creación de la **Guía Técnica** para desarrolladores (`Guía_Técnica_para_Desarrolladores.md`)
- Ajustes en `requirements` y documentación técnica
- Commits relacionados: `ad327cf`, `65500d1`, `cba16a7`, `7a974da`

**⏱ Duración estimada:** 1.5 días

---

## ⏳ **Resumen del tiempo estimado por módulo**

| Fase                     | Fechas                   | Duración estimada |
|--------------------------|--------------------------|-------------------|
| Preparación inicial      | 13 mayo                  | 1 día             |
| Ingesta y validación     | 13–14 mayo               | 1.5 días          |
| Limpieza y embeddings    | 14–15 mayo               | 2 días            |
| Vector DB                | 15 mayo                  | 1 día             |
| Búsqueda y ranking       | 14–20 mayo (intercalado) | 4–5 días          |
| Cierre y ajustes finales | 20–21 mayo               | 1.5 días          |
| Clustering y guía técnica| 21–22 mayo               | 1.5 días          |

---

### 🧾 **Conclusión actualizada**

El desarrollo de **Eval-IA** ha tomado aproximadamente **13–14 días efectivos**. La evolución del proyecto ha sido continua, con fases claras y objetivos bien delimitados. La incorporación del modelo de clustering y la documentación técnica refuerzan la madurez del sistema, orientado a escalabilidad y mantenimiento a largo plazo.

