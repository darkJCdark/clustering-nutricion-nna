# Paso 8 — Interpretación de patrones

**Estado:** documentado; pendiente de ejecutar
**Salida que pide el curso:** Hallazgos

| | |
|---|---|
| **Entrada** | `data/processed/07_etiquetas.csv`, `04_features.csv`, `07_comparacion.csv` |
| **Salida guardada** | `reports/figures/*.png`, `reports/tablas/08_perfiles.csv` y este `.md` |
| **Notebook** | `notebooks/08_interpretacion.ipynb` |

## Procedimiento

1. Perfil por cluster: media/mediana y dispersión de las numéricas; frecuencia de cada categoría; tamaño. Celdas con menos de 5 NNA se agrupan o se suprimen.
2. Comparar el perfil con los diagnósticos manuales (tabla cruzada agregada y ARI).
3. PCA o MDS **solo para visualizar**; indicar que no sustituyen el modelo.
4. Contrastar con la literatura ([6], [7]) y con el sentido de negocio. Si un perfil no tiene interpretación, volver al Paso 4–7.
5. Nombrar cada perfil en lenguaje del negocio (sin estigmatizar) y redactar qué acción de seguimiento sugiere, siempre como apoyo y no diagnóstico.

## Checklist del curso

- [ ] Perfil descriptivo de cada cluster con gráficos y métricas
- [ ] Visualización con PCA/MDS aclarando su límite
- [ ] Corroboración con literatura
- [ ] Interpretación interna antes de exponerla

## Registro de lo realizado

*(Se completa al ejecutar.)*

## Fuentes

[6] Oji-Onuoha et al. y [7] Kao et al. para el contexto; alcance y población en `fuentes/registro.md`.
