# Paso 2 — Creación del *target dataset*: selección y entendimiento

**Estado:** parte 1 ejecutada (diccionario y cobertura); estadísticos numéricos pendientes del Paso 3
**Salida que pide el curso:** Reporte de selección y descripción de variables

| | |
|---|---|
| **Entrada** | `data/raw/ficha_nominal/…v2.txt` y `data/raw/nutricion_mensual/*.xlsx` (tras `reordenar_repo.ps1`; mientras tanto, ruta original) |
| **Salida guardada** | `data/interim/02_diccionario.csv`, `data/interim/02_cobertura.csv` y este `.md` con el reporte |
| **Notebook** | `notebooks/02_seleccion_entendimiento.ipynb` |

## Qué debe hacer el notebook

1. Leer la ficha (`sep="|"`, UTF-8) y los 6 libros de nutrición (todas las hojas, buscando la fila de encabezado por el texto "APELLIDOS Y NOMBRES").
2. Construir `02_diccionario.csv` con las columnas `fuente, variable, escala, tipo_python, uso (M/V/X/K), motivo, vacios_pct, n_unicos`, partiendo de `docs/07_diccionario_de_datos.md`.
3. Construir `02_cobertura.csv`: NNA por mes, hogar y tramo etario (<5, 5–19); intersección ficha ∩ nutrición en enero 2026.
4. Estadísticos: cualitativas con frecuencia, porcentaje y moda; cuantitativas (peso, talla, IMC, edad) con tendencia central + dispersión + asimetría + curtosis; atípicos con cajas (asimétricas) o Z-score (simétricas).
5. Leer completos los PDF CENAN/OMS y anotar qué contienen (cortes o parámetros LMS) en el reporte.

## Checklist del curso

- [ ] Inventario de fuentes y variables; descartadas con motivo
- [ ] Escala y tipo en Python de cada variable
- [ ] Estadísticos descriptivos (cualitativas y cuantitativas)
- [ ] Atípicos detectados (sin tratar aún)
- [ ] Cobertura por mes, hogar y tramo etario
- [ ] Confirmar D1 y D2 con las cifras reales

## Criterios de salida (para pasar al Paso 3)

- `02_diccionario.csv` existe y cubre las 33 variables de la ficha y las columnas de cada hoja de nutrición.
- n por tramo etario en enero 2026 documentado. Si el tramo 5–19 tiene menos de ~100 NNA, se vuelve a decidir D1.

## Registro de lo realizado

2026-10-21: se escribió `src/config.py`, `src/lectura.py` y `scripts/paso02_seleccion.py` (y el notebook `notebooks/02_seleccion_entendimiento.ipynb`, que lo llama). Se ejecutó sobre copias de los archivos con Python 3.13 y pandas; la ejecución del notebook en Jupyter queda para el autor. Resultados (agregados):

- Ficha: 2 667 filas, 33 variables, 17 duplicados ID + periodo (parciales; ninguna fila completa repetida).
- Nutrición: 19 hojas en 6 libros; enero 2026: 141 NNA en libros, 137 en la ficha de ese mes, 4 sin ficha ese mes. Agosto de 2026 existe en los libros pero la ficha llega hasta julio.
- Diccionario con 52 entradas (33 de la ficha y 19 hojas de nutrición). Salidas en `data/interim/`.
- D1 y D2 se mantienen; el n del tramo 5–19 en enero se calcula en el Paso 3 al tener la edad por medición.

## Fuentes

Estadística descriptiva y atípicos: reglas del curso (`docs/04`). Sin fuente bibliográfica: DECISION del proyecto.
