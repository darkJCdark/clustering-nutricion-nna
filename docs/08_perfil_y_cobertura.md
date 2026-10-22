# Perfil de cobertura y decisiones que se derivan

Cálculos del 2026-10-21 sobre la ficha nominal y los libros de nutrición (solo agregados).

## Hallazgos

1. **Edad al último corte** (157 NNA): ≤5 años: 21; 5–10: 49; 10–15: 48; 15–20: 32; >20: 1. (Edad calculada con la fecha de nacimiento; 4 % de fechas no interpretables, por revisar.)
2. **El tramo <5 años tiene ~21 NNA.** Es insuficiente para comparar 3 algoritmos con k ≥ 3. El tramo 5–19 años tiene ~135 NNA.
3. **Hay tantas mediciones como libros, no como cortes de la ficha.** Mediciones por mes: enero 141, febrero 7, marzo 6, abril 108, junio 108, agosto 32. Enero es el **único corte completo** (todos los hogares).
4. La ficha de enero 2026 (`2026_01`) tiene 137 NNA, y los libros de enero 141: pueden faltar 4 NNA en la ficha de ese corte. Se cuantifica en el Paso 2.
5. Las filas repetidas por NNA son **medidas repetidas** de la misma persona: dividir train/test por fila produce fuga de información. La partición debe hacerse **por NNA**.
6. El diagnóstico `Nivel Nutricional` de la ficha y los diagnósticos manuales de los libros son resultados de tablas aplicadas a las mismas medidas: si entran al modelo, el clustering reproduce las tablas.

## Decisiones derivadas (borrador de Claude, ajustables)

| ID | Decisión | Motivo |
|---|---|---|
| D1 | **Unidad de análisis: un NNA** (corte transversal de **enero 2026**, n ≈ 141) | Único corte con todos los hogares; evita medidas repetidas |
| D2 | **Análisis principal en 5–19 años** (~135 NNA al último corte; el n exacto en enero 2026 se calcula en el Paso 2). El tramo <5 años se describe pero no se agrupa con los 3 algoritmos | Tamaño de muestra; son referencias de crecimiento distintas (OMS vs. CDC/CENAN) |
| D3 | Partición train/test **por NNA**, antes de cualquier análisis (propuesta 70/30 con semilla fija) | Curso (S7) y evitar fuga |
| D4 | Los diagnósticos manuales y `Nivel Nutricional` **no entran al modelo**: solo a validación externa (ARI) | Evitar circularidad |
| D5 | Trayectorias (abril, junio, agosto) quedan como **fase opcional**, solo si el análisis principal termina | Cobertura desigual por hogar |
| D6 | Variables administrativas y casi constantes quedan fuera (tabla del diccionario) | Sin varianza o riesgo de reidentificación |
| D7 | No se reduce dimensionalidad por defecto: se decide tras Bartlett/KMO con el número final de variables | Curso: reducir es opcional y pierde interpretación |

## Actualización tras el Paso 3 (2026-10-21)

- Enero 2026 con medida válida: **132 NNA** (112 en 5–19 años; 19 <5; 1 mayor de 19 por revisar). Con partición 70/30 por NNA quedan ≈ 78 en train y ≈ 34 en test en el tramo 5–19. Es una muestra pequeña: los resultados de estabilidad y de test tendrán alta variabilidad y deben reportarse con esa advertencia.
- D1 y D2 se mantienen. Si en el Paso 7 la estabilidad es baja, se evaluará ampliar con abril y junio (otra medición del mismo NNA, con partición **por NNA** para no filtrar información).
