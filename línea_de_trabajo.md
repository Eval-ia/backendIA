
## **Línea Temporal del Proyecto Eval-IA (13 al 21 de mayo de 2025)**


### 🟩 **Inicio y Preparación del Proyecto**

📅 **13 mayo 2025**

* Estructura inicial del repositorio creada (`Initial clean commit`, `README`, carpetas `app2_ia/`)
* Se realizaron múltiples merges de ramas vacías/iniciales.
* ✅ *Inicio del repositorio, estructura base, definición de módulos.*

**⏱ Duración estimada:** 1 día

---

### 🟦 **Módulo 1: Ingesta y Validación de CSV**

📅 **13–14 mayo 2025**

* Implementación del procesamiento CSV, validaciones básicas, detección de datos sensibles, logs (`defe4e1`, `56ac2d1`, `ea44e12`)
* Múltiples merges relacionados con `modulo_01` y `modulo2/utils`.

**⏱ Duración estimada:** 1.5 días

---

### 🟨 **Módulo 2–3: Limpieza de texto y generación de embeddings**

📅 **14–15 mayo 2025**

* Limpieza de texto con spaCy (`Función nueva`, `Quitamos schema no usado`)
* Embedding funcional y proyección (`Creación de embedding funcional`, `Mejoras Globales`, `Inserción en BD funcionando`)

**⏱ Duración estimada:** 2 días

---

### 🟧 **Módulo 4: Almacenamiento en vector DB con pgvector**

📅 **15 mayo 2025**

* Función de inserción en vector DB (`Insercción a la base de datos funciona correctamente`)
* Revisión de `requirements`, estructura final estable

**⏱ Duración estimada:** 1 día

---

### 🟥 **Módulo 5: Búsqueda vectorial y ranking por similitud**

📅 **14–20 mayo 2025**

* Desarrollo del endpoint `/buscar_similares` (`Controller y service búsqueda`, `calculo de similitud`)
* Control de duplicados, validaciones adicionales
* Refactorizaciones finales y mejoras (`version con límite en query`, `corrección duplicidad datos`)

**⏱ Duración estimada:** 4–5 días

---

### 🟪 **Fase Final y Estabilización**

📅 **20–21 mayo 2025**

* Se implementaron límites en la búsqueda y validación de resultados (`version_limite`)
* Merges finales y cierre de versiones (`Merge pull request #17`, `#16`, etc.)

**⏱ Duración estimada:** 1–1.5 días

---

## ⏳ **Resumen del tiempo estimado por módulo**

| Fase                     | Fechas                   | Duración estimada |
| ------------------------ | ------------------------ | ----------------- |
| Preparación inicial      | 13 mayo                  | 1 día             |
| Ingesta y validación     | 13–14 mayo               | 1.5 días          |
| Limpieza y embeddings    | 14–15 mayo               | 2 días            |
| Vector DB                | 15 mayo                  | 1 día             |
| Búsqueda y ranking       | 14–20 mayo (intercalado) | 4–5 días          |
| Cierre y ajustes finales | 20–21 mayo               | 1.5 días          |

---

### 🧾 Conclusión

El desarrollo de **Eval-IA** tomó aproximadamente **11–12 días efectivos**, con participación de múltiples colaboradores y commits bien distribuidos. Las fases técnicas fueron construidas de forma modular y escalonada, lo que favorece su mantenimiento y evolución futura.
