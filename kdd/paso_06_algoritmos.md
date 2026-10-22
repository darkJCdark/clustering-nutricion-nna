# Paso 6 — Elegir algoritmos y parámetros

**Estado:** documentado; los umbrales se fijan aquí **antes** de ver resultados
**Salida que pide el curso:** Lista de técnicas (mínimo 3) y escenarios de hiperparámetros

| | |
|---|---|
| **Entrada** | `data/processed/04_features.csv` |
| **Salida guardada** | `data/processed/06_plan_experimentos.csv` y este `.md` |
| **Notebook** | `notebooks/06_plan_algoritmos.ipynb` (genera el CSV y fija semillas) |

## Variables del modelo (candidatas, a confirmar tras el Paso 4)

- **Numéricas:** z de talla/edad, z de IMC/edad (o equivalentes del Paso 4), `edad_meses`, `meses_permanencia`.
- **Categóricas:** sexo, situación legal (agrupada), estudia, estado de salud física (agrupado), discapacidad (sí/no), soporte psico-emocional (agrupado), atención en salud mental especializada.
- **Ordinal:** último nivel educativo.
- **Fuera del modelo:** diagnósticos manuales y `Nivel Nutricional` (solo validación externa).

Tipo de cada variable definido explícitamente (el curso lo exige) en `06_plan_experimentos.csv`.

## Algoritmos (≥3) y escenarios

| # | Algoritmo | Entrada | Escenarios |
|---|---|---|---|
| A1 | K-Means (línea base) | Numéricas estandarizadas + dummies | k = 2…8; `n_init` = 20; 5 semillas |
| A2 | K-Prototypes (`kmodes`, init `Cao`) | Matriz mixta | k = 2…8; `n_init` ∈ {5, 10}; `max_iter` ∈ {100, 300}; codo del costo |
| A3 | Gower + jerárquico (enlace `average`) | Matriz Gower | corte para k = 2…8; dendograma |
| A4 | Gower + PAM (`KMedoids`, métrica precomputada) | Matriz Gower | k = 2…8; 5 semillas |
| A5 | Gower + DBSCAN / HDBSCAN | Matriz Gower | `eps` por codo de k-distancias; `min_samples` ∈ {3, 5}; −1 = ruido |

**Distancia:** Gower para mixtas, con pesos iguales por defecto y un análisis de sensibilidad con variables ordinales tratadas como ordinales vs. nominales. La literatura revisada ([1]) compara K-Prototypes con Gower+PAM y otros métodos en datos mixtos con ordinales; el alcance exacto se anota al leer el texto completo.

**Criterio común de comparación:** silhouette sobre la matriz Gower en train; desempate con Davies-Bouldin (cuando aplica), tamaño mínimo de cluster y silhouettes negativos por cluster.

## Reglas para elegir el mejor (fijadas antes de ver resultados)

1. Se descartan soluciones con un cluster <5 % de train o más de 20 % de silhouettes negativos. DECISION: umbrales del proyecto.
2. Entre las restantes, se elige la de mayor silhouette; si la diferencia con la siguiente es <0,02, se prefiere la más simple/interpretable.
3. Luego se optimiza solo el mejor (grilla fina de sus hiperparámetros) y se valida en test y estabilidad.

## Umbrales de aceptación (fijados el 2026-10-21 con las fuentes disponibles)

- **Silhouette:** valor de referencia ≈ 0,20 con k = 3, reportado por Heiskala et al. [4] al agrupar trayectorias de IMC infantil con k-medoids (resumen leído; población y datos distintos). Regla: la solución elegida debe alcanzar al menos ese valor de referencia; si no, se informa como estructura débil y no se interpretan perfiles como grupos definidos. Este umbral es una referencia de la literatura, no un estándar.
- **ARI (test y estabilidad):** no se encontró en Scopus (búsqueda 2026-10-21) una fuente con un umbral numérico. DECISION: criterio relativo y sin cifra mágica: (a) el ARI se compara con un **control de etiquetas permutadas** (esperado ≈ 0) y debe quedar claramente por encima; (b) entre modelos se prefiere el de mayor ARI medio de estabilidad; (c) se reporta la media y la desviación estándar, y se interpreta con el criterio del curso ("si un hallazgo se repite bajo pequeñas variaciones es más probable que sea real").
- **Tamaño y negativos:** ningún cluster <5 % de train; ≤20 % de silhouettes negativos. DECISION del proyecto (sin fuente).

## Validación (S7)

- Con test: KNN entrenado con etiquetas de train; predice test; ARI, Rand y Jaccard frente a los clusters de test.
- Estabilidad: submuestreo 80 % (≥30 repeticiones), bootstrap, ruido en numéricas, 20 semillas; ARI medio.
- Externa (informativa): ARI contra diagnósticos manuales.

## Checklist del curso

- [x] Mínimo 3 algoritmos compatibles con datos mixtos
- [x] Escenarios de hiperparámetros por algoritmo
- [x] Distancia y tipo de variable definidos
- [x] Criterio común de comparación
- [x] Plan de validación
- [x] Umbrales de aceptación fijados antes del Paso 7 (ver arriba); el autor los aprobó el 2026-10-21 ("sí a todo, basate en las fuentes")

## Registro de lo realizado

2026-10-21: plan redactado. Código pendiente.

## Fuentes

[1] Szepannek et al.; [2] Ghattas (preprint, solo como antecedente); [4] Heiskala (k-medoids); [5] Huang (K-Means de series). Chicco [3]: sin indexación confirmada, no se cita aún.
