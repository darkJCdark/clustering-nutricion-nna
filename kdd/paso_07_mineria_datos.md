# Paso 7 — Minería de datos (clustering)

**Estado:** documentado; pendiente de ejecutar
**Salida que pide el curso:** Modelos entrenados y tabla de comparación

| | |
|---|---|
| **Entrada** | `data/processed/04_features.csv`, `04_particion.csv`, `06_plan_experimentos.csv` |
| **Salida guardada** | `data/processed/07_modelos/`, `07_comparacion.csv`, `07_etiquetas.csv` (NNA → cluster; seudónimo), `07_validacion.csv` y este `.md` |
| **Notebooks** | `notebooks/07a_clustering_train.ipynb`, `07b_validacion_test.ipynb`, `07c_estabilidad.ipynb` |

## Procedimiento

1. Cargar solo `conjunto == train` para ajustar. Calcular la matriz Gower una vez y guardarla (`07_modelos/gower_train.npy`).
2. Ejecutar cada algoritmo y escenario del Paso 6. Registrar en `07_comparacion.csv`: algoritmo, hiperparámetros, k, silhouette global, silhouette mínimo por cluster, % silhouettes negativos, tamaño mínimo y máximo de cluster, Davies-Bouldin, tiempo.
3. Elegir k por codo y silueta como herramientas complementarias; aplicar las reglas del Paso 6.
4. Optimizar el mejor modelo (grilla fina) y guardar el modelo y su configuración.
5. Validar con test: KNN → ARI, Rand, Jaccard.
6. Estabilidad: submuestreo, bootstrap, ruido y semillas → ARI; reportar media y desviación.
7. Etiquetar todos los NNA y guardar `07_etiquetas.csv`.

## Entregables de código

`src/` con funciones reutilizables (ver `src/README.md`): lectura, normalización, Gower, wrappers de los algoritmos, métricas y estabilidad. Los notebooks solo orquestan y muestran **tablas agregadas y gráficos**; ninguna celda imprime filas individuales.

## Checklist del curso

- [ ] Partición train/test previa respetada
- [ ] Todos los algoritmos y escenarios ejecutados
- [ ] Silhouette global y por cluster; tamaños; negativos
- [ ] Validación con test (KNN + Rand, ARI, Jaccard)
- [ ] Estabilidad (subsampling, bootstrap, ruido, semillas) con ARI
- [ ] Optimización del mejor modelo
- [ ] Etiquetas guardadas

## Criterios de salida

`07_comparacion.csv` incluye ≥3 algoritmos con sus escenarios; `07_validacion.csv` incluye ARI de test y de estabilidad del modelo elegido.

## Registro de lo realizado

*(Se completa al ejecutar.)*

## Fuentes

Ver Paso 6.
