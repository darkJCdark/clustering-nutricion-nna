# Paso 3 — Limpieza y pre-procesamiento

**Estado:** ejecutado el 2026-10-21 (script); notebook escrito, sin ejecutar en Jupyter
**Salida que pide el curso:** Reporte de pre-procesamiento

| | |
|---|---|
| **Entrada** | `data/interim/02_diccionario.csv`, `data/raw/…` |
| **Salida guardada** | `data/interim/03_limpio.csv` (una fila por NNA y medición), `data/interim/03_log_limpieza.csv` y este `.md` |
| **Notebook** | `notebooks/03_limpieza.ipynb` |

## Reglas de limpieza ya identificadas

| Problema (fuente) | Regla |
|---|---|
| Fecha de nacimiento como fecha, texto `dd/mm/aaaa` o con hora (nutrición); 4 % no interpretable (ficha) | Parsear con formatos explícitos; no interpretable → vacío, con registro |
| Edad en texto libre (`4 años 10 meses`, `7año 5 meses`) | **No usarla**: recalcular `edad_meses` con fecha de nacimiento y fecha de medición |
| Espacios finales, mayúsculas, `\r\r`, tildes rotas (`Tècnico`) | `strip`, minúsculas, quitar saltos de línea, mapa de equivalencias |
| `*` en columnas de diagnóstico | Significa "no aplica": convertir a vacío con motivo `no_aplica` |
| `Si`/`si`/`SI`, `No aplicca` | Mapa de normalización por variable |
| Soporte psico-emocional (53 textos) y Nivel nutricional (31) | Normalizar y tokenizar combinaciones (`Acompañamiento/Psicoterapia`) |
| 17 duplicados ID + periodo | Conservar la fila más completa; registrar el resto |
| Encabezados distintos por hoja | Mapa explícito hoja → columnas estándar (`peso_kg, talla_cm, imc, dx_*`) |
| Peso y talla vacíos (hasta 17 % en Matogrosso) | Ver imputación |

## Faltantes y atípicos (procedimiento del curso)

1. Por variable: mecanismo MCAR / MAR / MNAR razonado y documentado.
2. Imputación solo si el vacío es ≤ 15–20 % por columna y por fila; peso y talla **no se imputan** (son la medida base): el NNA sin ellos se excluye. Categóricas: moda o categoría "Desconocido".
3. Comparar la distribución antes y después de imputar.
4. Atípicos de peso, talla e IMC: primero verificar si son error de digitación (IMC vs. peso/talla); tratar con flag o capping solo si es error; no abusar del capping.

## Checklist del curso

- [x] Duplicados completos y parciales tratados
- [x] Vacíos (espacio, cadena vacía, NaN) entendidos
- [x] Mecanismo de faltantes por variable
- [x] Imputación con tope y comparación antes/después
- [x] Atípicos tratados y comparados
- [x] Categorías normalizadas y fechas unificadas
- [x] Tabla maestra con una fila por NNA y medición

## Criterios de salida

- `03_limpio.csv` no contiene IDs duplicados por (ID, mes).
- Ninguna columna del modelo supera 20 % de vacíos.
- `03_log_limpieza.csv` lista cada transformación con su conteo de filas afectadas.

## Registro de lo realizado

2026-10-21: `src/limpieza.py`, `scripts/paso03_limpieza.py` y `notebooks/03_limpieza.ipynb`. Se ejecutó el script sobre copias (Python 3.13, pandas). Salidas en `data/interim/`: `03_limpio.csv` (402 mediciones, 141 NNA, seudonimizados, sin fechas ni distrito), `03_log_limpieza.csv`, `03_atipicos.csv`.

Resultados (agregados):
- Mediciones válidas (con peso, talla y edad): 379 de 402. Sin medida válida: 23 (9 en enero, 7 en abril, 7 en junio; todas en el tramo 5–19). No se imputaron.
- **Enero 2026 válido: 132 NNA** = 112 en 5–19 años, 19 en menores de 5 y 1 mayor de 19 (edad ≈ 28 años: probable error de fecha de nacimiento o caso especial; **revisar con el hogar**, queda fuera del análisis principal).
- Duplicados: 17 en la ficha (se conservó la fila con menos vacíos); 0 en nutrición.
- Unión con la ficha: 37 mediciones usaron la fila de ficha de un periodo cercano (incluye agosto, fuera del rango de la ficha, y 4 NNA sin ficha en enero); 0 sin ficha.
- Fechas de nacimiento: 0 no interpretables en los libros; en 6 mediciones las fechas de libros y ficha discrepan más de 31 días (se usó la del libro).
- Categorías normalizadas: situación legal (4 clases), salud física (3), soporte psico-emocional (5), salud mental especializada (3), discapacidad (binaria), nivel educativo (0–4). Diagnósticos manuales: errores de tipeo corregidos (`NORNAL`, `OBEESIDAD`, `RIEGO`, etc.); `*` -> vacío.
- Vacíos en columnas del modelo: 0 % tras filtrar mediciones válidas; no hubo imputación, por lo que no corresponde la comparación antes/después.
- Atípicos (tramo 5–19, n = 311 mediciones): peso 1 por IQR; IMC 7 por IQR (asimetría 1,0: se usa IQR); talla y edad ninguno. No se capean: pueden ser obesidad real. Menores de 5: ninguno.
- Edad mínima/máxima 5–19: 60,4 y 227,5 meses.

Supuesto: fecha de medición = día 15 del mes del libro (error de ±0,5 meses en la edad). DECISION.

## Fuentes

Reglas del curso (`docs/04`). Sin fuente bibliográfica: DECISION del proyecto.
