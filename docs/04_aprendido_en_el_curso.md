# Lo aprendido en el curso y cómo se aplica a este proyecto

Fuente: `teoria_1INF03_analisis_de_datos.md` (resumen de teoría del repositorio del curso `pucp-2026-2-1inf03-data-analysis`), y los notebooks de las semanas 7 y 8 (validación de clustering y datos mixtos). Las semanas 9 en adelante no se han revisado para este documento.

## 1. KDD de 9 pasos

Los pasos son secuenciales, pero siempre se puede volver a uno anterior. En el curso, 9 pasos equivalen a 9 notebooks. El curso tiene **entrega final, sin despliegue**.

| # | Paso | Salida que pide el curso | Archivo en este repo |
|---|---|---|---|
| 1 | Entendimiento del dominio y objetivos | Ficha técnica del proyecto | `kdd/paso_01_entendimiento_negocio.md` |
| 2 | Selección y entendimiento de datos (*target dataset*) | Reporte de selección + descripción de variables | `kdd/paso_02_seleccion_entendimiento_datos.md` |
| 3 | Limpieza y pre-procesamiento | Reporte de pre-procesamiento | `kdd/paso_03_limpieza_preprocesamiento.md` |
| 4 | Transformación y reducción de dimensiones | Archivo con variables transformadas y, si aplica, componentes/factores | `kdd/paso_04_transformacion_reduccion.md` |
| 5 | Elegir la tarea de minería de datos | Decisión documentada | `kdd/paso_05_tarea_mineria.md` |
| 6 | Elegir algoritmos y parámetros | Lista de técnicas (**mínimo 3**) | `kdd/paso_06_algoritmos.md` |
| 7 | Minería de datos | Modelos entrenados | `kdd/paso_07_mineria_datos.md` |
| 8 | Interpretación de patrones | Hallazgos | `kdd/paso_08_interpretacion.md` |
| 9 | Consolidación del conocimiento | Informe final en términos del negocio | `kdd/paso_09_consolidacion.md` |

Aclaración del docente: *target data set* no es la variable objetivo; es el conjunto de datos con el que se trabajará. Los pasos 5 a 7 son el data mining.

## 2. Reglas del curso por paso y su aplicación

### Paso 1 — Entendimiento del negocio
- El problema se plantea **como pregunta**, expresa una relación entre variables y permite prueba empírica (Kerlinger y Lee, 2002, según el curso).
- Se distinguen **objetivos del negocio** y **objetivos de análisis de datos**, y se definen métricas de evaluación desde el inicio.
- Se delimita la población **en espacio y tiempo**, con criterios de **inclusión, exclusión y eliminación**.
- Se declaran recursos y limitaciones (personas, datos, herramientas; normativa de datos sensibles, tiempo).
- **Aplicación:** población = NNA de los hogares con evaluación nutricional mensual en 2025–2026. Limitación explícita: datos sensibles de menores y tamaño de muestra (~157 NNA distintos).

### Paso 2 — Selección y entendimiento
- Clasificar cada variable por naturaleza y escala (nominal, ordinal, intervalo, razón). En Python, `string ≠ object ≠ category`.
- Cualitativas: frecuencia absoluta, relativa, porcentaje y moda. Cuantitativas: **al menos una medida de tendencia central y una de dispersión**, más asimetría y curtosis. Pareja media ↔ desviación estándar; mediana ↔ RIC.
- Atípicos: **cajas (Q1 − 1.5·RIC, Q3 + 1.5·RIC)** si la distribución es asimétrica; **Z-score (±3 s)** si es simétrica.
- **Aplicación:** diccionario de variables con escala; peso, talla, IMC y edad son de razón; los diagnósticos manuales son nominales u ordinales.

### Paso 3 — Pre-procesamiento
- Duplicados (completos y parciales por ID + fecha). Vacíos (`" "`, `""`, `NaN`): entender por qué hay vacíos.
- Faltantes: **MCAR, MAR, MNAR**; imputación univariada, condicional o multivariada (KNN, iterativa); **tope de vacíos de 15–20 %** por columna y por fila; **comparar la distribución antes y después** de imputar.
- Atípicos: trimming, capping (winsorización), imputación, transformación, flag. No abusar del capping.
- Categóricas: moda o categoría nueva ("Desconocido").
- **Aplicación:** unificar formatos mensuales, normalizar categorías (`Si`/`si`/`SI`, saltos de línea), tratar fechas. Documentar el mecanismo de cada vacío.

### Paso 4 — Transformación y reducción
- **Normalizar ≠ estandarizar.** Min-Max, Z, robusta (mediana/RIC), logaritmo. No aplicar una transformación masiva sin analizar variable por variable; guardar el objeto de transformación.
- La reducción de dimensiones **no es obligatoria** y pierde interpretabilidad. PCA exige variables numéricas, prueba de esfericidad de **Bartlett** (p < 0.05) y estandarización. EFA exige además **KMO ≥ 0.5–0.6**, número de factores, rotación (Varimax) y nombre de los factores.
- **Aplicación:** estandarizar solo las numéricas; los percentiles/puntaje z de la OMS ya son comparables entre edades. Evaluar Bartlett/KMO antes de decidir si se reduce.

### Pasos 5 y 6 — Tarea y algoritmos
- La tarea se elige **emparejando con el Paso 1**: predictiva, descriptiva u optimización. Clustering es **descriptiva y no supervisada**.
- Elegir **mínimo 3 algoritmos** y, dentro de cada uno, varios escenarios de hiperparámetros. Definir nosotros el tipo de variable.
- **Aplicación:** tarea descriptiva (perfiles nutricionales); lista de algoritmos ver sección 3.

### Paso 7 — Clustering (Step 7a)
- Objetivo: grupos **homogéneos por dentro y heterogéneos entre sí**. Todo se basa en distancias, así que hay que estandarizar.
- Distancias: Euclidiana, Manhattan, Minkowski, Chebyshev, Canberra, **Gower** (mixtas). Mahalanobis para atípicos multivariados.
- Jerárquicos: **AGNES / DIANA**, dendograma con cortes, enlace Ward o average. Particionales: **K-means** (sensible a atípicos y a la inicialización: usar varias), **PAM** (medoides, robusto), **CLARA** (grandes), **FANNY** (difuso).
- Elegir k con **codo (inercia) y silueta (−1 a 1)** como herramientas complementarias, más criterio de negocio. Mirar silueta global, por cluster, tamaños homogéneos y pocos valores negativos.
- Cerrar: etiquetar, **describir cada cluster**, usar PCA solo para visualizar.
- Con **datos mixtos** (S8): matriz de **Gower** (`gower`), **K-Prototypes** (`kmodes`, init `Cao`, codo del costo, grilla de K / n_init / max_iter; no usa D directamente), **Gower + jerárquico** (`linkage` con `average`), **Gower + PAM** (`KMedoids`, métrica precomputada), **Gower + DBSCAN** (eps por el codo de la distancia al k-ésimo vecino; etiqueta −1 = ruido) y **Gower + HDBSCAN**. Evaluar todos con **silhouette sobre la matriz Gower** como criterio común. **MDS** solo para visualizar: puede crear separaciones que el modelo no respalda.

### Validación (S7)
- Análisis **exploratorio** (patrones, anomalías) y **confirmatorio** (corroborar con literatura, datos de test, estabilidad, experimentos).
- **Validación con test:** dividir train/test **antes** del análisis; hallar k clusters en train; entrenar un clasificador (KNN) con las etiquetas de train; predecir test; comparar con los clusters de test mediante **Rand, ARI y Jaccard**.
- **Estabilidad:** "si un hallazgo se repite bajo pequeñas variaciones, es más probable que sea real". Perturbaciones: subsampling (80 %), bootstrapping, ruido, corrupciones aleatorias, inicializaciones y semillas distintas; medir con ARI.

### Pasos 8 y 9
- Interpretar en bucle con el paso 7, internamente antes de exponerlo; reportar en **términos del negocio**.

## 3. Plan de algoritmos para este proyecto (a aprobar en el Paso 6)

Variables mixtas (numéricas antropométricas + categóricas de contexto). Candidatos, todos vistos en el curso:

| Algoritmo | Insumo | Observación |
|---|---|---|
| K-Means | Variables numéricas estandarizadas | Línea base; sensible a atípicos |
| K-Prototypes | Matriz mixta | Codo del costo; init `Cao` |
| Gower + jerárquico (average) | Matriz Gower | Dendograma; detecta atípicos |
| Gower + PAM (KMedoids) | Matriz Gower | Robusto a atípicos |
| Gower + DBSCAN / HDBSCAN | Matriz Gower | Ruido (−1); eps por codo de k-distancias |

Comparación común: silhouette sobre la matriz Gower. Validación: partición train/test previa, clasificador KNN y ARI/Jaccard, y estabilidad con perturbaciones.

## 4. Condiciones de evaluación del curso

- Nota final = (30·Pb + 30·Ta + 20·Ex1 + 20·Ex2) / 100. La Tarea Académica (Ta) se desarrolla sobre un proyecto real con una institución aliada.
- El uso de IA generativa debe declararse y citarse; el docente puede pedir el reporte de prompts como anexo.
- El plagio tiene nota cero.
- Bibliografía obligatoria: Knaflic; Larose y Larose; Fayyad et al. (1996); Marz; Duda, Hart y Stork.
